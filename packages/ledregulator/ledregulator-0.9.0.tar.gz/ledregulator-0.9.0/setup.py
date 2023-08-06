# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ledregulator']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.61.1,<0.62.0', 'uvicorn>=0.11.8,<0.12.0']

entry_points = \
{'console_scripts': ['runserver = ledregulator.runserver:main']}

setup_kwargs = {
    'name': 'ledregulator',
    'version': '0.9.0',
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
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
