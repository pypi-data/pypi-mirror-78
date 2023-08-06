# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'python'}

packages = \
['cognite',
 'cognite.seismic',
 'cognite.seismic._api',
 'cognite.seismic.data_classes',
 'cognite.seismic.protos']

package_data = \
{'': ['*']}

install_requires = \
['cognite-geospatial-sdk>=0.1.8,<0.2.0',
 'deprecation>=2.1.0,<3.0.0',
 'grpcio-tools>=1.31,<2.0',
 'numpy>=1.17,<2.0',
 'pip>=20.2.2,<21.0.0',
 'protobuf>=3.12,<4.0',
 'python-dateutil>=2.8,<3.0',
 'setuptools>=49.0,<50.0',
 'six>=1.14,<2.0',
 'urllib3>=1.24,<2.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

setup_kwargs = {
    'name': 'cognite-seismic-sdk',
    'version': '0.1.59',
    'description': '',
    'long_description': None,
    'author': 'cognite',
    'author_email': 'support@cognite.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
