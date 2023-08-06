# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cdm_classes']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cdm-classes',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'mountain',
    'author_email': 'tim@lustberg.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
