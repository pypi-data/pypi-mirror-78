# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lowclouds']

package_data = \
{'': ['*']}

extras_require = \
{'bigquery': ['google-cloud-bigquery>=1.27.2,<2.0.0',
              'google-cloud-bigquery-storage>=1.0.0,<2.0.0',
              'grpcio>=1.31.0,<2.0.0']}

setup_kwargs = {
    'name': 'lowclouds',
    'version': '0.1.1',
    'description': 'The lowclouds is a shortcut library for the following cloud service libraries.',
    'long_description': '# lowclouds\n\nThe lowclouds is a shortcut library for several cloud service libraries.\n\nIt is designed for processes with short lifetimes, not for processes with long lifetimes.\n\n',
    'author': 'rhoboro',
    'author_email': 'rhoboro@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
