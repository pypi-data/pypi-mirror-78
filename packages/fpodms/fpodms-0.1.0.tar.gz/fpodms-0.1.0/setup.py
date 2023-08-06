# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fpodms']

package_data = \
{'': ['*']}

install_requires = \
['inflection>=0.5.1,<0.6.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'fpodms',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Charlie Bini',
    'author_email': 'cbini87@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
