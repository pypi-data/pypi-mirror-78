# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pocketutils',
 'pocketutils.biochem',
 'pocketutils.core',
 'pocketutils.logging',
 'pocketutils.misc',
 'pocketutils.notebooks',
 'pocketutils.plotting',
 'pocketutils.tools']

package_data = \
{'': ['*']}

install_requires = \
['importlib_metadata>=1.7,<2.0', 'tomlkit>=0.7,<1.0']

extras_require = \
{'all': ['dill>=0.3,<1.0',
         'jsonpickle>=1,<2',
         'joblib>=0.16,<1.0',
         'numpy>=1.18,<2.0',
         'pandas>=1.1,<2.0',
         'matplotlib>=3.3,<4.0',
         'goatools>=1,<2',
         'requests>=2,<3',
         'uniprot>=1.3,<2.0',
         'colorama>=0.4,<1.0',
         'psutil>=5,<6',
         'ipython>=7,<8'],
 'biochem': ['numpy>=1.18,<2.0',
             'pandas>=1.1,<2.0',
             'goatools>=1,<2',
             'requests>=2,<3',
             'uniprot>=1.3,<2.0'],
 'misc': ['colorama>=0.4,<1.0', 'psutil>=5,<6'],
 'notebooks': ['pandas>=1.1,<2.0', 'ipython>=7,<8'],
 'plotting': ['matplotlib>=3.3,<4.0'],
 'tools': ['dill>=0.3,<1.0',
           'jsonpickle>=1,<2',
           'joblib>=0.16,<1.0',
           'numpy>=1.18,<2.0',
           'pandas>=1.1,<2.0']}

setup_kwargs = {
    'name': 'pocketutils',
    'version': '0.2.0',
    'description': 'Adorable little Python code for you to copy or import.',
    'long_description': '# pocketutils\n\n[![Version status](https://img.shields.io/pypi/status/pocketutils)](https://pypi.org/project/pocketutils/)\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pocketutils)](https://pypi.org/project/pocketutils/)\n[![Docker](https://img.shields.io/docker/v/dmyersturnbull/pocketutils?color=green&label=DockerHub)](https://hub.docker.com/repository/docker/dmyersturnbull/pocketutils)\n[![GitHub release (latest SemVer including pre-releases)](https://img.shields.io/github/v/release/dmyersturnbull/pocketutils?include_prereleases&label=GitHub)](https://github.com/dmyersturnbull/pocketutils/releases)\n[![Latest version on PyPi](https://badge.fury.io/py/pocketutils.svg)](https://pypi.org/project/pocketutils/)\n[![Documentation status](https://readthedocs.org/projects/pocketutils/badge/?version=latest&style=flat-square)](https://pocketutils.readthedocs.io/en/stable/)\n[![Build & test](https://github.com/dmyersturnbull/pocketutils/workflows/Build%20&%20test/badge.svg)](https://github.com/dmyersturnbull/pocketutils/actions)\n[![Maintainability](https://api.codeclimate.com/v1/badges/eea2b741dbbbb74ad18a/maintainability)](https://codeclimate.com/github/dmyersturnbull/pocketutils/maintainability)\n[![Coverage](https://coveralls.io/repos/github/dmyersturnbull/pocketutils/badge.svg?branch=master)](https://coveralls.io/github/dmyersturnbull/pocketutils?branch=master)\n\nAdorable little Python functions for you to copy or import.\n\n`pip install pocketutils`. To get the optional packages, use:\n`pip install pocketutils[tools,biochem,misc,notebooks,plotting]`\n\nAmong the more useful are `zip_strict`, `frozenlist`, `SmartEnum`, `is_lambda`, `strip_paired_brackets`,\n`sanitize_path_node`, `TomlData`, `PrettyRecordFactory`, `parallel_with_cursor`, `groupby_parallel`,\n`loop_timing`, and `stream_cmd_call`.\n\nAlso has functions for plotting, machine learning, and bioinformatics.\nSome of the more useful are `ConfusionMatrix`, `DecisionFrame`,\n[`PeakFinder`](https://en.wikipedia.org/wiki/Topographic_prominence), `AtcParser` (for PubChem ATC codes),\n`WellBase1` (for multiwell plates), and [`TissueTable`]("https://www.proteinatlas.org/).\n\n[See the docs](https://pocketutils.readthedocs.io/en/stable/), or just\n[browse the code](https://github.com/dmyersturnbull/pocketutils/tree/master/pocketutils).\n\n[New issues](https://github.com/dmyersturnbull/pocketutils/issues) and pull requests are welcome.\nPlease refer to the [contributing guide](https://github.com/dmyersturnbull/pocketutils/blob/master/CONTRIBUTING.md).\nGenerated with [Tyrannosaurus](https://github.com/dmyersturnbull/tyrannosaurus).\n',
    'author': 'Douglas Myers-Turnbull',
    'author_email': None,
    'maintainer': 'Douglas Myers-Turnbull',
    'maintainer_email': None,
    'url': 'https://github.com/dmyersturnbull/pocketutils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
