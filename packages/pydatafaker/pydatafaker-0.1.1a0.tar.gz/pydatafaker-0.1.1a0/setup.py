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
    'version': '0.1.1a0',
    'description': 'A python package to create fake data with relationships between tables.',
    'long_description': '# pydatafaker\nA python package to create fake data with relationships between tables.\n\n## Notes for developers\n\nHelpful reminders for PyDataFaker developers\n\n### Create a new release\n\n```bash\npoetry version patch # see https://python-poetry.org/docs/cli/#version\npoetry run pytest\npoetry build\npoetry publish\n```\n\n### Updating the documentation\n\n```bash\npoetry run sphinx-apidoc -f -o docs/source pydatafaker\ncd docs\npoetry run make html\n```\n',
    'author': 'Sam Edwardes',
    'author_email': 'edwardes.s@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
