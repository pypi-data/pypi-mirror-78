# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['breaktimer']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'pyfiglet>=0.8.post1,<0.9', 'rich>=6.0.0,<7.0.0']

setup_kwargs = {
    'name': 'breaktimer',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Joben R',
    'author_email': 'joben.rara@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
