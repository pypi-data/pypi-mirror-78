# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['doif']
install_requires = \
['rich>=5.2.0,<6.0.0']

entry_points = \
{'doif': ['main = doif:src/main']}

setup_kwargs = {
    'name': 'doif',
    'version': '0.3.0',
    'description': 'TryHackMe',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
