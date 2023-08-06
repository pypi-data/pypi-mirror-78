# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['glacier']

package_data = \
{'': ['*']}

install_requires = \
['click-help-colors>=0.8,<0.9', 'click>=7.1.2,<8.0.0']

setup_kwargs = {
    'name': 'glacier',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Hiroki Konishi',
    'author_email': 'relastle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
