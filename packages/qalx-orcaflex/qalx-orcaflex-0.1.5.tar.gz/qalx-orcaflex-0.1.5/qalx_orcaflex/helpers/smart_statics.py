"""
Smart Statics
~~~~~~~~~~~~~

Smart statics allows users to add tags to objects in an OrcaFlex model to enable an
iterative search for a model that solves in statics.

This is to overcome the common issue where a model that initially solves in statics
fails to do so after a small change to the model data. Usually this is fixed in one of
a few ways:

- the user adjusts some damping
- the user moves a line end around
- the user changes the statics method

Smart statics gives users the ability to define what they would try in the model and
 when the model is run in `bots.SimBot` the bot will try to find a static solution.

It does this by calling `solved_model` which is documented below.
"""
import collections
import json
from itertools import cycle
from logging import getLogger
from pprint import pformat
from typing import Sequence, Union, Mapping

import numpy as np
from OrcFxAPI import stStaticsFailed, Model, DLLError

from qalx_orcaflex.helpers import get_tags

logger = getLogger("pyqalx.integration")
logger.setLevel("DEBUG")


def gather_search_criteria(model: Model) -> Sequence[Union[Mapping, None]]:
    """parses the object tags to get the search criteria and any sequence.

    :param model: ofx.Model
    :return: list of; Object -> list of Data Item mappings or None
    """
    search = collections.defaultdict(dict)
    for search_obj, search_terms in get_tags(
        model, lambda t: t.startswith("ss_"), True
    ).items():
        for term, adjust in search_terms.items():
            parts = term[3:].split("__")
            if len(parts) == 2:
                data_name, index = parts[0], int(parts[1])
            else:
                data_name, index = parts[0], 0
            search[search_obj][(data_name, index)] = {
                "initial_value": model[search_obj].GetData(data_name, index),
                "adjustment": adjust,
            }
    search_sequence = []
    for _, seq_terms in get_tags(
        model, lambda t: t.startswith("SEARCH_SEQUENCE__")
    ).items():
        for sequence_number, object_filter in seq_terms.items():
            if object_filter.lower() == "all":
                search_sequence.insert(int(sequence_number.split("__")[-1]), None)
            else:
                search_sequence.insert(
                    int(sequence_number.split("__")[-1]), json.loads(object_filter)
                )
    return search, search_sequence


def apply_absolute_adjustment(obj, data_name, index, initial_value, adjustment):
    """sets the data value to a random value between adjustment['min']
    and adjustment['max'].

    It uses the initial value either is undefined.
    """
    min = adjustment.get("min", initial_value)
    max = adjustment.get("max", initial_value)
    if min == max:
        raise ArithmeticError(f"min and max are equal ({min})")
    value = np.random.uniform(min, max)
    logger.info(f"Setting {data_name}[{index}] to {value}")
    obj.SetData(data_name, index, value)
    return data_name, index, value


def apply_nudge(obj, data_name, index, adjustment):
    """sets the data value in a increment defined by adjustment['distance']
    """
    last_value = obj.GetData(data_name, index)
    value = last_value + adjustment["distance"]
    logger.info(f"Setting {data_name}[{index}] to {value}")
    obj.SetData(data_name, index, value)
    return data_name, index, value


def apply_choice(obj, data_name, index, choices):
    """sets the data value by selecting at random from choices.

    """
    value = np.random.choice(choices)
    logger.info(f"Setting {data_name}[{index}] to {value}")
    obj.SetData(data_name, index, value)
    return data_name, index, value


def apply_cycle_choices(obj, data_name, index, choice_cycle):
    """sets the data value by selecting in turn from choice_cycle.

    choice_cycle is simply itertools.cycle(adjustment['choices'])
    """
    value = next(choice_cycle)
    logger.info(f"Setting {data_name}[{index}] to {value}")
    obj.SetData(data_name, index, value)
    return data_name, index, value


def apply_all_adjustments(model, search, cycles, object_filter=None):
    """applies adjustments to the model as extracted from tags to search.

    Object filter should be a list of Object Name:List[Data Name] mappings to be
    adjusted. An empty list of data names will adjust all data names.
    If object_filter is left unspecified, all objects will be adjusted.
    """
    if object_filter is None:
        object_filter = {k: [] for k in search.keys()}
    for obj_name in object_filter:
        adjustments = search[obj_name]
        if not object_filter[obj_name]:
            data_names = [n for (n, i) in adjustments.keys()]
        else:
            data_names = object_filter[obj_name]
        obj_to_adjust = model[obj_name]
        adjustments_required = {
            (n, i): v for (n, i), v in adjustments.items() if n in data_names
        }
        for (data_name, index), adjustment_info in adjustments_required.items():
            adjustment = adjustment_info["adjustment"]
            initial_value = adjustment_info["initial_value"]
            if adjustment["type"] == "absolute":
                setting = apply_absolute_adjustment(
                    obj_to_adjust, data_name, index, initial_value, adjustment
                )
            elif adjustment["type"] == "nudge":
                setting = apply_nudge(obj_to_adjust, data_name, index, adjustment)
            elif adjustment["type"] == "choice":
                setting = apply_choice(
                    obj_to_adjust, data_name, index, adjustment["choices"]
                )
            elif adjustment["type"] == "cycle":
                if (obj_name, data_name, index) not in cycles:
                    cycles[(obj_name, data_name, index)] = cycle(adjustment["choices"])
                setting = apply_cycle_choices(
                    obj_to_adjust,
                    data_name,
                    index,
                    cycles[(obj_name, data_name, index)],
                )
            model.general.Comments += (
                f"\n{setting[0]}[{setting[1]}] set to " f"{setting[2]}"
            )


def reset_model(model, search):
    """resets all adjusted parameters in the search

    :param model:
    :param search:
    :return:
    """
    for obj_name, data_adjustments in search.items():
        obj = model[obj_name]
        for (data_name, index), adjustment_info in data_adjustments.items():
            obj.SetData(data_name, index, adjustment_info["initial_value"])


def perform_search(model, search, max_attempts, object_filter=None):
    """iterate up to max_attempts to find a model that solved

    :param model: ofx.Model
    :param search: search params
    :param max_attempts: number of attempts
    :param object_filter: objects and data items to try
    :return: tuple of ofx.Model and True or False depending on whether the model solves
    """
    attempts = 0
    cycles = {}
    model.general.Comments += f"\n***\nSMART STATICS with {pformat(dict(search))}\n***"
    while attempts < max_attempts:
        attempts += 1
        model.general.Comments += f"\n---\nSMART STATICS ATTEMPT {attempts}:"
        apply_all_adjustments(model, search, cycles, object_filter)
        try:
            model.CalculateStatics()
            return model, True
        except DLLError as err:
            if err.status == stStaticsFailed:
                logger.info(f"Attempt {attempts} failed.")
            else:
                raise err
    reset_model(model, search)
    return model, False


def solved_model(model, max_attempts=10, save_path=None):
    """tries to solve a model in statics, if it fails a search will be performed for
    a solution based on object tags.

    The search is based on tags placed on objects in the model and optionally a
    sequence of object filters to apply.

    To specify a search, add tags to the object you want to be adjusted.
    The tag name must start with "ss\_" followed by the data name to be adjusted
    then optionally a double underscore ("__") and the index.
    If no index is given then the first row (zero index) will be adjusted.

    The value of the tag must be a json string containing the type of adjustment from
     one of the following options:

        - "type": "absolute"
            the data value will be set to a random absolute value between
             "min" and "max" if only one is specified then
             the initial model value is assumed to be the other limit.
        - "type": "nudge"
            the data value will be changed incrementally by "distance" on each attempt
        - "type": "cycle"
            the data value will be set by cycling through all the "choices" in turn
        - "type": "choice"
            the data value will be set to a random selection of "choices"

    You can restrict the objects and data names that are adjusted in a sequence by
    adding tags to General. These must
    start with `SEARCH_SEQUENCE__` and then have a number so `SEARCH_SEQUENCE__1`,
    `SEARCH_SEQUENCE__2` etc. The value
    of the tag must be either `ALL` or a string that contains a mappings of objects
    to data items that should be
    adjusted. For example

        SEARCH_SEQUENCE__1 => {'General':['StaticsMinDamping']}
        SEARCH_SEQUENCE__2 => {'Line1':[]}
        SEARCH_SEQUENCE__3 => {'General':[], 'Line1':[]}
        SEARCH_SEQUENCE__4 => ALL

    will try to solve by adjusting only StaticsMinDamping in General, then all data
    names in Line1
    and then both General and Line1 at the same time. `All` will try to adjust all
    objects.


    Some examples:

        setting model['General'].tags['ss_StaticsMinDamping'] to
        '{"type":"nudge", "distance":1}' will add one to the
        minimum full model statics damping each attempt.

        setting model['Line1'].tags['ss_FullStaticsMinDamping'] to '{"type":"cycle",
        "choices":[1,3,5]}' will
        set the Line1 minimum damping to 1 then 3 then 5 then back to 1 and so on.

        setting model['Line1'].tags['ss_EndBZ'] to '{"type":"absolute", "max":-20}'
        will set the Line1
        z coordinate of End B to a random value between the initial value and -20.

    :param model: OrcFxAPI.Model
    :param max_attempts: number of attempts to make
    :param save_path: filepath to save the solved model
    :return: an OrcFxAPI.Model that solves in statics.
    """
    try:
        model.CalculateStatics()
        return model
    except DLLError as err:
        if err.status == stStaticsFailed:
            search, search_sequence = gather_search_criteria(model)
            if not search_sequence:
                filters = [None]
            else:
                filters = search_sequence
            while filters:
                model, solves = perform_search(
                    model, search, max_attempts, filters.pop(0)
                )
                if solves:
                    if save_path:
                        model.SaveData(save_path)
                    return model
            else:
                raise DLLError(
                    stStaticsFailed,
                    f"No solution found after"
                    f" {max_attempts} attempts on {len(filters)} filters.",
                )
