# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['argufy']

package_data = \
{'': ['*']}

install_requires = \
['argparse_color_formatter>=1.2.2,<2.0.0', 'docstring-parser>=0.7.2,<0.8.0']

setup_kwargs = {
    'name': 'argufy',
    'version': '0.1.1.dev10',
    'description': 'Inspection based parser based on argparse.',
    'long_description': None,
    'author': 'Jesse P. Johnson',
    'author_email': 'jpj6652@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
