# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ledregulator']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.61.1,<0.62.0', 'uvicorn>=0.11.8,<0.12.0']

setup_kwargs = {
    'name': 'ledregulator',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'DonQueso89',
    'author_email': 'kg.v.ekeren@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
