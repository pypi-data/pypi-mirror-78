# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['agtest']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.16.0,<0.17.0',
 'click>=7.1.2,<8.0.0',
 'pandas>=1.1.1,<2.0.0',
 'parse>=1.17.0,<2.0.0',
 'regobj>=0.2.2,<0.3.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['agtest = agtest.cli:main']}

setup_kwargs = {
    'name': 'agtest',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'MrSuperbear',
    'author_email': 'fraser.darrin@gmail.com',
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
