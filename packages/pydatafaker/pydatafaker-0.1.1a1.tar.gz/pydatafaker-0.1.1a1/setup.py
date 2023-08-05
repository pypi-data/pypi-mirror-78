# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydatafaker']

package_data = \
{'': ['*']}

install_requires = \
['faker>=4.1.2,<5.0.0', 'pandas>=1.1.1,<2.0.0']

setup_kwargs = {
    'name': 'pydatafaker',
    'version': '0.1.1a1',
    'description': 'A python package to create fake data with relationships between tables.',
    'long_description': None,
    'author': 'Sam Edwardes',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
