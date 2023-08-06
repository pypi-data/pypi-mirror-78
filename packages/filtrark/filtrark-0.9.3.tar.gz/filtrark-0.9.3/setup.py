# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['filtrark']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'filtrark',
    'version': '0.9.3',
    'description': 'Build filter clauses from instruction lists',
    'long_description': None,
    'author': 'Knowark',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
