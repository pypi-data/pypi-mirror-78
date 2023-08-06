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
    'version': '0.1.1',
    'description': 'Python abstraction around Binary Decision Diagrams to implement Multivalued Decision Diagrams.',
    'long_description': '# Py-MDD\n\nPython abstraction around Binary Decision Diagrams to implement\nMultivalued Decision Diagrams.\n\n[![Build Status](https://cloud.drone.io/api/badges/mvcisback/py-mdd/status.svg)](https://cloud.drone.io/mvcisback/py-mdd)\n[![codecov](https://codecov.io/gh/mvcisback/py-mdd/branch/master/graph/badge.svg)](https://codecov.io/gh/mvcisback/py-mdd)\n[![PyPI version](https://badge.fury.io/py/py-mdd.svg)](https://badge.fury.io/py/mdd)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n\n# Installation\n\nIf you just need to use `py-mdd`, you can just run:\n\n`$ pip install mdd`\n\nFor developers, note that this project uses the\n[poetry](https://poetry.eustace.io/) python package/dependency\nmanagement tool. Please familarize yourself with it and then\nrun:\n\n`$ poetry install`\n\n\n# Usage\n\n```python\n    interface = mdd.Interface(\n        inputs={\n            "x": [1, 2, 3],\n            "y": [6, \'w\'], \n            "z": [7, True, 8],\n        }, \n        output=[-1, 0, 1],\n    )\n    func = interface.constantly(-1)\n    assert func({\'x\': 1, \'y\': \'w\', \'z\': 8}) == -1\n```\n\nThe `mdd` api centers around three `DecisionDiagram` objects.\n\n  This\nobject is a wrapper around a Binary Decision Diagram object (from\n[dd](https://github.com/tulip-control/dd)).\n\n\n# Interfaces, Inputs, and Outputs\n\n# MDD Manipulations\n1. [ ] partial assigments.\n1. [ ] overrides.\n1. [ ] setting order.\n1. [ ] wrapping lifting a bdd.\n\n# Variables and Encodings\n\n\n',
    'author': 'Marcell Vazquez-Chanlatte',
    'author_email': 'mvc@linux.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mvcisback/py-mdd',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
