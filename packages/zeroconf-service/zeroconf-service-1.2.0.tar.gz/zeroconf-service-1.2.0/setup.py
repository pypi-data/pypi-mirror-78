# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zeroconf_service']

package_data = \
{'': ['*']}

install_requires = \
['compress-pickle[lz4]>=1.2.0,<2.0.0',
 'websockets>=8.1,<9.0',
 'zeroconf>=0.28.3,<0.29.0']

setup_kwargs = {
    'name': 'zeroconf-service',
    'version': '1.2.0',
    'description': '',
    'long_description': None,
    'author': 'Tim Wedde',
    'author_email': 'timwedde@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
