# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graphql_framework']

package_data = \
{'': ['*'], 'graphql_framework': ['templates/graphql_framework/*']}

install_requires = \
['graphql-core>=3']

setup_kwargs = {
    'name': 'django-gql-framework',
    'version': '0.1.7',
    'description': '',
    'long_description': None,
    'author': 'Ellis Percival',
    'author_email': 'flyte@failcode.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
