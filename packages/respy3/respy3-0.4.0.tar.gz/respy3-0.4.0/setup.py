# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['respy3']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'respy3',
    'version': '0.4.0',
    'description': 'A RESP3 protocol parser for Python',
    'long_description': None,
    'author': 'Harrison Morgan',
    'author_email': 'harrison.morgan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
