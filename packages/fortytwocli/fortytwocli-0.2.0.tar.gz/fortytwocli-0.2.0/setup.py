# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fortytwocli']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.3,<4.0.0',
 'click>=7.1.2,<8.0.0',
 'halo>=0.0.29,<0.0.30',
 'inquirer>=2.6.3,<3.0.0',
 'rich>=6.0.0,<7.0.0']

entry_points = \
{'console_scripts': ['42 = fortytwocli.main:fourtyTwo']}

setup_kwargs = {
    'name': 'fortytwocli',
    'version': '0.2.0',
    'description': 'command line tool for 42 intra.',
    'long_description': '',
    'author': 'Hibiki Okada',
    'author_email': 'hokada@student.42tokyo.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dhaiibfiukkiu/42cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
