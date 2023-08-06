# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['papurika']

package_data = \
{'': ['*']}

install_requires = \
['grpcio-tools>=1.26.0,<2.0.0', 'grpcio>=1.26.0,<2.0.0']

setup_kwargs = {
    'name': 'papurika',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Hanaasagi',
    'author_email': 'ambiguous404@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
