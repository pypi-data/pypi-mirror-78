# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eventz']

package_data = \
{'': ['*']}

install_requires = \
['immutables>=0.14,<0.15', 'python-dateutil>=2.8.1,<3.0.0']

setup_kwargs = {
    'name': 'eventz',
    'version': '0.3.0',
    'description': 'Eventz: an event-centric microframework.',
    'long_description': None,
    'author': 'Dan Ballance',
    'author_email': 'work@danballance.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
