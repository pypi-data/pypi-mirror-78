# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['solconfig']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'jinja2>=2.11.2,<3.0.0', 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['solconfig = solconfig.cmd:cli']}

setup_kwargs = {
    'name': 'solconfig',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'flyisland',
    'author_email': 'flyisland@gmail.com',
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
