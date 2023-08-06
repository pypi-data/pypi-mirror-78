# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['stats_can']

package_data = \
{'': ['*']}

install_requires = \
['h5py>=2.10.0,<3.0.0',
 'pandas>=1.1.0,<2.0.0',
 'requests>=2.20,<3.0',
 'tables>=3.6.1,<4.0.0',
 'tqdm>=4.48.0,<5.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.7.0,<2.0.0']}

setup_kwargs = {
    'name': 'stats-can',
    'version': '2.3.4',
    'description': 'Read StatsCan data into python, mostly pandas dataframes',
    'long_description': "# Python api for Statistics Canada New Data Model (NDM)\n\n[![Tests](https://github.com/ianepreston/stats_can/workflows/Tests/badge.svg)](https://github.com/ianepreston/stats_can/actions?workflow=Tests)\n[![Documentation Status](https://readthedocs.org/projects/stats-can/badge/?version=latest)](https://stats-can.readthedocs.io/en/latest/?badge=latest)\n[![codecov](https://codecov.io/gh/ianepreston/stats_can/branch/master/graph/badge.svg)](https://codecov.io/gh/ianepreston/stats_can)\n[![Anaconda-Server Badge](https://anaconda.org/ian.e.preston/stats_can/badges/installer/conda.svg)](https://conda.anaconda.org/ian.e.preston)\n[![Anaconda-Server Badge](https://anaconda.org/ian.e.preston/stats_can/badges/version.svg)](https://anaconda.org/ian.e.preston/stats_can)\n[![Anaconda-Server Badge](https://anaconda.org/ian.e.preston/stats_can/badges/platforms.svg)](https://anaconda.org/ian.e.preston/stats_can)\n[![Anaconda-Server Badge](https://anaconda.org/ian.e.preston/stats_can/badges/license.svg)](https://anaconda.org/ian.e.preston/stats_can)\n\nAPI documentation for StatsCan can be found here: https://www.statcan.gc.ca/eng/developers/wds\n\nIf you're looking for Table/Vector IDs to use in the app you can find them through this:\nhttps://www150.statcan.gc.ca/n1/en/type/data\n\nAnaconda package here:\nhttps://anaconda.org/ian.e.preston/stats_can\n\n\nDocumentation here:\nhttps://stats-can.readthedocs.io/en/latest/\n",
    'author': 'Ian Preston',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ianepreston/stats_can',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
