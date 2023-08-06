# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jrpyprogramming', 'jrpyprogramming.datasets']

package_data = \
{'': ['*'],
 'jrpyprogramming': ['vignettes/*'],
 'jrpyprogramming.datasets': ['data/*']}

install_requires = \
['matplotlib>=3.0', 'numpy>=1.14.4', 'pandas>=0.23']

setup_kwargs = {
    'name': 'jrpyprogramming',
    'version': '0.1.12',
    'description': 'Jumping Rivers: Python Programming',
    'long_description': None,
    'author': 'Jamie',
    'author_email': 'jamie@jumpingrivers.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
