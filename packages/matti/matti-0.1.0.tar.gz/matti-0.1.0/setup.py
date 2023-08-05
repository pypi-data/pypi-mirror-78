# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['matti']

package_data = \
{'': ['*']}

install_requires = \
['black>=20.8b1,<21.0']

setup_kwargs = {
    'name': 'matti',
    'version': '0.1.0',
    'description': 'pattern match',
    'long_description': None,
    'author': 'sh1ma',
    'author_email': 'in9lude@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sh1ma/matti',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
