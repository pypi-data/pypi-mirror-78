# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['majocol']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.1,<2.0.0',
 'opencv-python>=4.4.0,<5.0.0',
 'scikit-learn>=0.23.2,<0.24.0']

setup_kwargs = {
    'name': 'majocol',
    'version': '0.1.1',
    'description': 'pick major colors from image',
    'long_description': '# MajoCol\n\npick major colors from image\n',
    'author': 'suzukey',
    'author_email': 'suzukey28@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/suzukey/majocol',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
