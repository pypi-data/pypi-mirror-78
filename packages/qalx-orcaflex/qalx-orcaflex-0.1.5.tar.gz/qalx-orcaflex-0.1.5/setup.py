# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qalx_orcaflex',
 'qalx_orcaflex.bots',
 'qalx_orcaflex.bots.batch',
 'qalx_orcaflex.bots.sim',
 'qalx_orcaflex.core',
 'qalx_orcaflex.data_models',
 'qalx_orcaflex.helpers']

package_data = \
{'': ['*']}

install_requires = \
['OrcFxAPI>=11.0.2,<12.0.0',
 'pandas>=1.0.4,<2.0.0',
 'psutil>=5.7.0,<6.0.0',
 'pyqalx>=0.12.0',
 'pyyaml>=5.3.1,<6.0.0']

extras_require = \
{'docs': ['sphinx>=2.1,<3.0', 'sphinx-rtd-theme>=0.4.3,<0.5.0'],
 'pip-licenses': ['pip-licenses>=1.16,<2.0']}

setup_kwargs = {
    'name': 'qalx-orcaflex',
    'version': '0.1.5',
    'description': 'qalx Bots and helpers for OrcaFlex by Orcina',
    'long_description': None,
    'author': 'Steven Rossiter',
    'author_email': 'steve@agiletek.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
