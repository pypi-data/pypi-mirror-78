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
    'version': '0.2.1',
    'description': 'command line tool for 42 intra.',
    'long_description': '# 42cli\n\n<p align="center"><img src="https://user-images.githubusercontent.com/40907120/83941623-cb867900-a827-11ea-970f-1058c0fdd303.png"></p>\n<p align="center">\n<img src="https://img.shields.io/badge/-Linux-grey?logo=linux">\n<img src="https://img.shields.io/badge/-OSX-black?logo=apple">\n<img src="https://circleci.com/gh/dhaiibfiukkiu/42cli/tree/master.svg?style=shield&circle-token=e5c59d1e8f71cd2535bb75c675af70944385dd57">\n<a href="https://codecov.io/gh/dhaiibfiukkiu/42cli">\n  <img src="https://codecov.io/gh/dhaiibfiukkiu/42cli/branch/master/graph/badge.svg?token=AYUREEQZJI" />\n</a>\n<a href="https://github.com/dhaiibfiukkiu/42cli/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/dhaiibfiukkiu/42cli"></a>\n<a href="https://github.com/dhaiibfiukkiu/42cli/network"><img alt="GitHub forks" src="https://img.shields.io/github/forks/dhaiibfiukkiu/42cli"></a>\n<a href="https://github.com/dhaiibfiukkiu/42cli/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/dhaiibfiukkiu/42cli"></a>\n<a href="https://github.com/dhaiibfiukkiu/42cli/blob/master/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/dhaiibfiukkiu/42cli"></a>\n<a href="https://pypi.org/project/fortytwocli/">\n<img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/fortytwocli"><a/>\n<a href="https://pypi.org/project/fortytwocli/">\n<img alt="PyPI" src="https://img.shields.io/pypi/v/fortytwocli"></a>\n<a href="https://pypi.org/project/fortytwocli/">\n<img alt="PyPI" src="https://pepy.tech/badge/fortytwocli"></a>\n</p>\n<p align="center">command line tool for 42 intra.</p>\n<p align="right">\nIcons made by <a href="https://www.flaticon.com/authors/dave-gandy" title="Dave Gandy">Dave Gandy</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>\n</p>\n\n<!--# DEMO-->\n\n<!--# Features-->\n\n# Requirement\n* Python3.8.2\n\n# Installation\n```pip install fortytwocli```\n\n<!--# Usage-->\n\n# FAQ\n## how to activate shell completion?\nHere is activation script.\n```\neval "$(_42_COMPLETE=source_bash 42)" \n```\nIf you use zsh, you just need to replace `source_bash` with `source_zsh`.\n\n\n# Author\nhokada\n<<hokada@student.42tokyo.jp>>\n\n# License\n"42cli" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).\n',
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
