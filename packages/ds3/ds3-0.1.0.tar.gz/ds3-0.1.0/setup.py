# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ds3']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ds3',
    'version': '0.1.0',
    'description': 'The S3 API for Python',
    'long_description': None,
    'author': 'Tomas Pereira de Vasconcelos',
    'author_email': 'tomasvasconcelos1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
