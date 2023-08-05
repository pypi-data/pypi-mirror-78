# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['perimod']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'perimod',
    'version': '1.0.1',
    'description': 'Peridot module maker in Python',
    'long_description': None,
    'author': 'Totobird',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
