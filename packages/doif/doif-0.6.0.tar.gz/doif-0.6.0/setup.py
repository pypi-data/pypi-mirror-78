# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['doif']

package_data = \
{'': ['*']}

install_requires = \
['rich>=5.2.0,<6.0.0']

entry_points = \
{'console_scripts': ['doif = doif.main:main']}

setup_kwargs = {
    'name': 'doif',
    'version': '0.6.0',
    'description': 'TryHackMe',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
