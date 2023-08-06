# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wizsdk']

package_data = \
{'': ['*']}

install_requires = \
['asyncio>=3.4.3,<4.0.0',
 'numpy>=1.19.1,<2.0.0',
 'opencv-python>=4.4.0,<5.0.0',
 'wizwalker>=0.12.2,<0.13.0']

setup_kwargs = {
    'name': 'wizsdk',
    'version': '0.1.2',
    'description': 'API for interacting with and making bots for wizard101',
    'long_description': None,
    'author': 'Underpaid Dev',
    'author_email': 'underpaiddev1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
