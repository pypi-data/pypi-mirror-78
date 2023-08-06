# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gogogate2_api']

package_data = \
{'': ['*']}

install_requires = \
['defusedxml>=0.6.0',
 'pycryptodomex>=3.9.7',
 'requests>=2.23.0',
 'typing-extensions>=3.7.4.2']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

entry_points = \
{'console_scripts': ['gogogate2 = gogogate2_api.cli:gogogate2_cli',
                     'ismartgate = gogogate2_api.cli:ismartgate_cli']}

setup_kwargs = {
    'name': 'gogogate2-api',
    'version': '2.0.1',
    'description': 'Library for connecting to GogoGate2 and iSmartGate hubs',
    'long_description': '# Python gogogate2-api [![Build status](https://github.com/vangorra/python_gogogate2_api/workflows/Build/badge.svg?branch=master)](https://github.com/vangorra/python_gogogate2_api/actions?workflow=Build) [![codecov](https://codecov.io/gh/vangorra/python_gogogate2_api/branch/master/graph/badge.svg)](https://codecov.io/gh/vangorra/python_gogogate2_api) [![PyPI](https://img.shields.io/pypi/v/gogogate2-api)](https://pypi.org/project/gogogate2-api/)\nPython library for controlling GogoGate2 and iSmartGate devices\n\n\n## Installation\n\n    pip install gogogate2-api\n\n## Usage in Commands\n```shell script\n$ gogogate2 --help\nUsage: gogogate2 [OPTIONS] COMMAND [ARGS]...\n\n  Interact with the device API.\n\nOptions:\n  --host TEXT      [required]\n  --username TEXT  [required]\n  --password TEXT  Omit for interactive prompt. Use \'-\' to read from stdin.\n  --version        Show the version and exit.\n  --help           Show this message and exit.\n\nCommands:\n  close  Close the door.\n  info   Get info from device.\n  open   Open the door.\n\n\n$ ismartgate --help\nUsage: ismartgate [OPTIONS] COMMAND [ARGS]...\n\n  Interact with the device API.\n\nOptions:\n  --host TEXT      [required]\n  --username TEXT  [required]\n  --password TEXT  Omit for interactive prompt. Use \'-\' to read from stdin.\n  --version        Show the version and exit.\n  --help           Show this message and exit.\n\nCommands:\n  close  Close the door.\n  info   Get info from device.\n  open   Open the door.\n```\n\n## Usage in Code\n```python\nfrom gogogate2_api import GogoGate2Api, ISmartGateApi\n\n# GogoGate2 API\ngogogate2_api = GogoGate2Api("10.10.0.23", "admin", "password")\n\n# Get info about device and all doors.\ngogogate2_api.info()\n\n# Open/close door.\ngogogate2_api.open_door(1)\ngogogate2_api.close_door(1)\n\n\n# iSmartGate API\nismartgate_api = ISmartGateApi("10.10.0.24", "admin", "password")\n\n# Get info about device and all doors.\nismartgate_api.info()\n\n# Open/close door.\nismartgate_api.open_door(1)\nismartgate_api.close_door(1)\n```\n\n## Building\nBuilding, testing and linting of the project is all done with one script. You only need a few dependencies.\n\nDependencies:\n- python3 in your path.\n- The python3 `venv` module.\n\nThe build script will setup the venv, dependencies, test and lint and bundle the project.\n```bash\n./scripts/build.sh\n```\n',
    'author': 'Robbie Van Gorkom',
    'author_email': 'robbie.van.gorkom@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vangorra/python_gogogate2_api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
