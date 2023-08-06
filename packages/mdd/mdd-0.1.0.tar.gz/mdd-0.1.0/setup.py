# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdd']

package_data = \
{'': ['*']}

install_requires = \
['dd>=0.5.5,<0.6.0',
 'funcy>=1.14,<2.0',
 'py-aiger-bdd>=3.0.0,<4.0.0',
 'py-aiger-bv>=4.3.0,<5.0.0',
 'py-aiger>=6.1.1,<7.0.0']

setup_kwargs = {
    'name': 'mdd',
    'version': '0.1.0',
    'description': 'Python abstraction around Binary Decision Diagrams to implement Multivalued Decision Diagrams.',
    'long_description': None,
    'author': 'Marcell Vazquez-Chanlatte',
    'author_email': 'mvc@linux.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
