from time import sleep

from pyqalx import Bot, Set, Group
from pyqalx.bot import QalxJob

from qalx_orcaflex.bots.batch.summaries import ResultsSummariser
from qalx_orcaflex.data_models import BatchOptions


def process_batch(job: QalxJob):
    """main batch processing function

    This will pull a batch off the queue and submit the sims if they haven't been submitted yet.
    """
    job.entity["meta"]["state"] = "processing"
    job.save_entity()
    options = BatchOptions(**job.entity["meta"]["options"])
    tasks = job.entity["sets"]
    if not job.entity["meta"].get(
        "sims_submitted"
    ):  # if the sims haven't been submitted yet
        sim_queue = job.session.queue.get_or_create(options.sim_queue)  # get the queue
        for task, s in tasks.items():  # add them all to the queue
            if not isinstance(s, Set):
                s = job.session.set.get(s)
                job.entity["sets"][task] = s
            Set.add_to_queue(payload=s, queue=sim_queue)
            s["meta"]["state"]["state"] = "Queued"
            s["meta"]["state"]["info"] = options.sim_queue
            job.session.set.save(s)
            job.log.debug(f"added {s['guid']} to {options.sim_queue}.")
        job.entity["meta"][
            "sims_submitted"
        ] = True  # set the flag so next time around we don't resubmit them
        job.save_entity()

    job.log.debug(f"batch {job.e['guid']} loaded.")


def send_batch_to(job: QalxJob, options: BatchOptions):
    """will send the entity on the job to all the queues defined in
    options.send_batch_to

    :param job:
    :param options:
    :return: None
    """
    if options.send_batch_to:
        for q_name in options.send_batch_to:
            queue = job.session.queue.get_or_create(q_name)
            job.entity.__class__.add_to_queue(payload=job.entity, queue=queue)


def post_process_batch(job: QalxJob):
    job.reload_entity()
    options = BatchOptions(**job.entity["meta"]["options"])
    tasks = job.entity["sets"]
    if not isinstance(list(tasks.values())[0], Set):
        tasks = {s: job.session.set.get(guid) for s, guid in tasks.items()}
    # Here we check to see if all the jobs have been processes by SimBots (or children)
    process_sets = [
        job.session.set.reload(e)["meta"].get("processing_complete")
        for s, e in tasks.items()
    ]
    job.log.debug(process_sets)
    # if they are all complete and we are supposed to do a results summary then crack on
    if (
        all(process_sets)
        and options.summarise_results
        and (not job.entity["meta"].get("results_summary"))
    ):
        job.entity["meta"]["state"] = "post-processing"
        job.save_entity()
        job.log.debug(f"batch {job.e['guid']} about to be summarised.")
        res_sum = ResultsSummariser(job)
        res_sum.summarise_batch(tasks)
        job.entity["meta"]["state"] = "processing_complete"
        job.log.debug(f"batch {job.e['guid']} summary complete.")
        job.save_entity()
        send_batch_to(job, options)
    elif options.summarise_results and (not job.entity["meta"].get("results_summary")):
        # if we do want to summarise this batch then let's wait for a bit and
        # then submit this job back to the batch
        # queue. It will eventually get back to this point and check again if
        # all jobs are complete.
        sleep(options.wait_between_completion_checks)
        batch_queue = job.session.queue.get_or_create(options.batch_queue)
        Group.add_to_queue(payload=job.entity, queue=batch_queue)
        job.log.debug(f"put batch {job.e['guid']} back on {options.batch_queue}.")
    else:  # we've done all we were supposed to do here
        job.entity["meta"]["state"] = "processing_complete"
        job.save_entity()
        send_batch_to(job, options)


class BatchBot(Bot):
    """batch processing bot

    Will start by submit jobs to the sim worker queue if they haven't been already.

    If `data_models.BatchOptions.summarise_results` is set to True then it will check
    if all the sims are complete. If they are not it puts the job back on the
    queue. If they are complete then it calls the summarise results functions.
    """

    def __init__(self, bot_name):
        super(BatchBot, self).__init__(bot_name)

        self.process_function = process_batch
        self.postprocess_function = post_process_batch
