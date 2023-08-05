# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chancepy']

package_data = \
{'': ['*']}

install_requires = \
['pytz>=2020.1,<2021.0']

setup_kwargs = {
    'name': 'chancepy',
    'version': '0.1.0',
    'description': 'Random generator helper for Python',
    'long_description': None,
    'author': 'Nuni',
    'author_email': 'nuni@kovrr.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
