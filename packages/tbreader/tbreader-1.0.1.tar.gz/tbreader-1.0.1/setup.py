# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tbreader', 'tbreader.proto']

package_data = \
{'': ['*']}

install_requires = \
['protobuf>=3.8.0']

setup_kwargs = {
    'name': 'tbreader',
    'version': '1.0.1',
    'description': 'A simple parser for tensorboard files',
    'long_description': None,
    'author': 'Daniel Suess',
    'author_email': 'daniel@dsuess.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
