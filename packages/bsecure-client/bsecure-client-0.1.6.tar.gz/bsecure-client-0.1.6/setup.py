# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bsecure_client', 'bsecure_client.api']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'bsecure-client',
    'version': '0.1.6',
    'description': 'BeSecure Client',
    'long_description': None,
    'author': 'william chu',
    'author_email': 'william.chu@uptickhq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
