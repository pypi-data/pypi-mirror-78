# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pgdiff']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'networkx>=2.4,<3.0',
 'psycopg2>=2.8.5,<3.0.0',
 'typing_extensions>=3.7.4,<4.0.0']

entry_points = \
{'console_scripts': ['pgdiff = pgdiff.cli:cli']}

setup_kwargs = {
    'name': 'pgdiff',
    'version': '0.1.20.post1',
    'description': '',
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
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
