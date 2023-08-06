# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['piri_cli']

package_data = \
{'': ['*']}

install_requires = \
['piri>=1.0.2,<2.0.0',
 'returns>=0.14.0,<0.15.0',
 'simplejson>=3.17.2,<4.0.0',
 'typing_extensions>=3.7.4,<4.0.0']

entry_points = \
{'console_scripts': ['piri = piri_cli.cli:main']}

setup_kwargs = {
    'name': 'piri-cli',
    'version': '0.1.9',
    'description': 'Piri Json Transformer CLI',
    'long_description': None,
    'author': 'Thomas Borgen',
    'author_email': 'thomas@borgenit.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
