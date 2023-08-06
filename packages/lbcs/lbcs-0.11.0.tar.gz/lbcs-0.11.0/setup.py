# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lbcs']

package_data = \
{'': ['*']}

install_requires = \
['tornado>=6.0.4,<7.0.0']

entry_points = \
{'console_scripts': ['lbcs-server = lbcs.server:main']}

setup_kwargs = {
    'name': 'lbcs',
    'version': '0.11.0',
    'description': 'A small async server for processing led commands to AdaFruit Neopixels',
    'long_description': None,
    'author': 'Kees van Ekeren',
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
