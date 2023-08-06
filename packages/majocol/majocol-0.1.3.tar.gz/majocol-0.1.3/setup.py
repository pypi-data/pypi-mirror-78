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
    'version': '0.1.3',
    'description': 'pick major colors from image',
    'long_description': '<p align="center">\n  <img width="420px" src="https://raw.githubusercontent.com/suzukey/majocol/main/docs/img/majocol.png" alt=\'majocol\'>\n</p>\n\n<p align="center">\n  <em>Pick major colors from image</em>\n</p>\n\n<p align="center">\n  <a href="https://pypi.org/project/majocol/" target="_blank">\n    <img src="https://badge.fury.io/py/majocol.svg" alt="Package version">\n  </a>\n</p>\n\n---\n\n**Documentation**:\n\n**Demo**:\n\n---\n\n# MajoCol\n\n## Requirements\n\nPython 3.6+\n\n## Installation\n\n```shell\n$ pip3 install majocol\n```\n\n<p align="center">&mdash; \U0001fa84 &mdash;</p>\n\n<p align="center">\n  <i>MajoCol is licensed under the terms of the <a href="https://github.com/suzukey/majocol/blob/main/LICENSE">MIT license</a>.</i>\n</p>\n',
    'author': 'suzukey',
    'author_email': 'suzukey28@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/suzukey/majocol',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
