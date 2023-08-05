# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_diceware']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['diceware = simple_diceware.simple_diceware:main']}

setup_kwargs = {
    'name': 'simple-diceware',
    'version': '0.3.0',
    'description': 'Create diceware passwords from the command line',
    'long_description': None,
    'author': 'Ben Chopson',
    'author_email': 'bchopson@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
