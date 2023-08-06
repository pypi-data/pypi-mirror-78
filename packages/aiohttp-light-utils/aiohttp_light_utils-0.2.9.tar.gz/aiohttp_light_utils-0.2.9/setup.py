# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiohttp_light_utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp_graphql>=1.0.0,<2.0.0',
 'graphene-file-upload>=1.2.2,<2.0.0',
 'graphene>=2.1.8,<3.0.0',
 'jsonrpcclient[aiohttp]>=3.3,<4.0',
 'pymongo>=3.9,<4.0',
 'python-json-logger>=0.1.11,<0.2.0',
 'trafaret-config>=2.0,<3.0',
 'ujson>=1.35,<2.0']

setup_kwargs = {
    'name': 'aiohttp-light-utils',
    'version': '0.2.9',
    'description': '',
    'long_description': None,
    'author': 'Khaziev Radik',
    'author_email': 'xazrad@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
