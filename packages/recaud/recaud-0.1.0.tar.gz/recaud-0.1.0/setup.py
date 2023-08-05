# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['recaud']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=5.3.1,<6.0.0']

setup_kwargs = {
    'name': 'recaud',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'dkllrjr',
    'author_email': 'dg.kllr.jr@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
