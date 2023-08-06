# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['aiopen']

package_data = \
{'': ['*']}

install_requires = \
['funkify>=0.0.1,<0.0.2']

setup_kwargs = {
    'name': 'aiopen',
    'version': '0.1.2',
    'description': 'Funkify modules so that they are callable',
    'long_description': None,
    'author': 'jesse',
    'author_email': 'jesse@dgi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dynamic-graphics-inc/dgpy-libs',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
