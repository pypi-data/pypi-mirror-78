# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioguardian', 'aioguardian.commands', 'aioguardian.helpers']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0',
 'async_timeout>=3.0.1,<4.0.0',
 'asyncio_dgram>=1.0.1,<2.0.0',
 'voluptuous>=0.11.7,<0.12.0']

setup_kwargs = {
    'name': 'aioguardian',
    'version': '1.0.2',
    'description': 'A Python3 library for Elexa Guardian water valves and sensors',
    'long_description': '# 🚰 aioguardian: A Python3 library for Elexa Guardian devices\n\n[![CI](https://github.com/bachya/aioguardian/workflows/CI/badge.svg)](https://github.com/bachya/aioguardian/actions)\n[![PyPi](https://img.shields.io/pypi/v/aioguardian.svg)](https://pypi.python.org/pypi/aioguardian)\n[![Version](https://img.shields.io/pypi/pyversions/aioguardian.svg)](https://pypi.python.org/pypi/aioguardian)\n[![License](https://img.shields.io/pypi/l/aioguardian.svg)](https://github.com/bachya/aioguardian/blob/master/LICENSE)\n[![Code Coverage](https://codecov.io/gh/bachya/aioguardian/branch/master/graph/badge.svg)](https://codecov.io/gh/bachya/aioguardian)\n[![Maintainability](https://api.codeclimate.com/v1/badges/a03c9e96f19a3dc37f98/maintainability)](https://codeclimate.com/github/bachya/aioguardian/maintainability)\n[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)\n\n`aioguardian` is a Python3, `asyncio`-focused library for interacting with\n[the Guardian line of water valves and sensors from Elexa](http://getguardian.com).\n\n- [Installation](#installation)\n- [Python Versions](#python-versions)\n- [Documentation](#documentation)\n- [Contributing](#contributing)\n\n# Installation\n\n```python\npip install aioguardian\n```\n\n# Python Versions\n\n`aioguardian` is currently supported on:\n\n* Python 3.6\n* Python 3.7\n* Python 3.8 \n\n# Documentation\n\nComplete documentation can be found here: http://aioguardian.readthedocs.io\n\n# Contributing\n\n1. [Check for open features/bugs](https://github.com/bachya/aioguardian/issues)\n  or [initiate a discussion on one](https://github.com/bachya/aioguardian/issues/new).\n2. [Fork the repository](https://github.com/bachya/aioguardian/fork).\n3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`\n4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`\n5. Install the dev environment: `script/setup`\n6. Code your new feature or bug fix.\n7. Write tests that cover your new functionality.\n8. Run tests and ensure 100% code coverage: `script/test`\n9. Update `README.md` with any new documentation.\n10. Add yourself to `AUTHORS.md`.\n11. Submit a pull request!\n',
    'author': 'Aaron Bach',
    'author_email': 'bachya1208@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bachya/aioguardian',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
