# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymortar']

package_data = \
{'': ['*']}

install_requires = \
['googleapis-common-protos>=1.5,<2.0',
 'grpcio-tools>=1.18,<2.0',
 'grpcio>=1.18,<2.0',
 'pandas>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'pymortar',
    'version': '1.0.9a2',
    'description': 'Python tool for Mortar testbed',
    'long_description': None,
    'author': 'Gabe Fierro',
    'author_email': 'gtfierro@cs.berkeley.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
