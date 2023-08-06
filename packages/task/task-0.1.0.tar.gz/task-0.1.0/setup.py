# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['task']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'task',
    'version': '0.1.0',
    'description': 'Task cli tool',
    'long_description': None,
    'author': 'matteyeux',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
