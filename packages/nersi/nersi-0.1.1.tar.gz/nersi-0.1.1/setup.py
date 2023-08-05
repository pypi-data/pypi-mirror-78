# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nersi']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.1,<4.0.0', 'networkx>=2.5,<3.0']

setup_kwargs = {
    'name': 'nersi',
    'version': '0.1.1',
    'description': 'A package for easily calculating the Network-Extended Residual Supply Index (NERSI), a measure of market concentration and pivotality for nodal electricity networks.',
    'long_description': None,
    'author': 'Luke Marshall',
    'author_email': 'lukasmarshall@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
