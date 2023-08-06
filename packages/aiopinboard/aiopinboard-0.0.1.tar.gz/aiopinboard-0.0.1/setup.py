# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiopinboard']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0', 'async_timeout>=3.0.1,<4.0.0', 'maya>=0.6.1,<0.7.0']

setup_kwargs = {
    'name': 'aiopinboard',
    'version': '0.0.1',
    'description': 'A Python 3, asyncio-based library for the Pinboard API',
    'long_description': '# 📌 aiopinboard: A Python 3, asyncio-based library for the Pinboard API\n\n`aioguardian` is a Python3, `asyncio`-based library for interacting with\n[Pinboard](https://pinboard.in) API.\n',
    'author': 'Aaron Bach',
    'author_email': 'bachya1208@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bachya/aiopinboard',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
