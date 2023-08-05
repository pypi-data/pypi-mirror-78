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
    'version': '0.4.1',
    'description': 'Create diceware passwords from the command line',
    'long_description': '# Simple Diceware\n\nCreate diceware-style passwords from the command line. \n\nWordlist copied from https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt\n\n### Install\n\n`pip install --user simple-diceware`\n\n### Use\n\n`diceware 6` to generate six-word passphrase\n',
    'author': 'Ben Chopson',
    'author_email': 'bchopson@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bchopson/simple-diceware',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
