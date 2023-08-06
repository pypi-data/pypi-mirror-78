# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gqlgen']

package_data = \
{'': ['*']}

install_requires = \
['click>=7,<8', 'graphql-core>=3']

entry_points = \
{'console_scripts': ['gqlgen = gqlgen.main:main']}

setup_kwargs = {
    'name': 'gqlgen',
    'version': '0.0.6',
    'description': 'Auto-generate GraphQL Type, Resolver and Query.',
    'long_description': None,
    'author': 'syfun',
    'author_email': 'sunyu418@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/syfun',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
