# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['perimod']
setup_kwargs = {
    'name': 'perimod',
    'version': '1.0.0',
    'description': 'Peridot module maker in Python',
    'long_description': None,
    'author': 'Totobird',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
