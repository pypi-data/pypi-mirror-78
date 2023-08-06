# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jrpyoop', 'jrpyoop.datasets']

package_data = \
{'': ['*'], 'jrpyoop': ['vignettes/*']}

install_requires = \
['matplotlib>=3.1,<4.0', 'pandas>=0.23.4,<0.24.0']

setup_kwargs = {
    'name': 'jrpyoop',
    'version': '0.1.7',
    'description': 'Jumping Rivers: Object-Oriented Programming in Python',
    'long_description': None,
    'author': 'Colin',
    'author_email': 'colin@jumpingrivers.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
