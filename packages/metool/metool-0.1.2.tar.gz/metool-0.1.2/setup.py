# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['metool']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'uuid>=1.30,<2.0']

entry_points = \
{'console_scripts': ['notebook = metool.notebook:main']}

setup_kwargs = {
    'name': 'metool',
    'version': '0.1.2',
    'description': 'Command tool for work and study.',
    'long_description': None,
    'author': 'Albert Chen',
    'author_email': 'albert.chen.dao@gmail.com',
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
