# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['purgeraw']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'mypy>=0.782,<0.783',
 'pylint>=2.6.0,<3.0.0',
 'toolz>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['praw = purgeraw.main:main']}

setup_kwargs = {
    'name': 'purgeraw',
    'version': '1.0.2',
    'description': '',
    'long_description': None,
    'author': 'Andy Phelps',
    'author_email': 'andrew.m.phelps@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
