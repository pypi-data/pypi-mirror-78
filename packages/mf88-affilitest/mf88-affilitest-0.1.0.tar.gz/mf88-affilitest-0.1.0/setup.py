# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mf88_affilitest']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'mf88-affilitest',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'vutr',
    'author_email': 'me@vutr.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.5,<4.0.0',
}


setup(**setup_kwargs)
