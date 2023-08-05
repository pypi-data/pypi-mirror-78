# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['chess_stats', 'chess_stats.models']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['chess-stats = chess_stats.console:main']}

setup_kwargs = {
    'name': 'chess-stats',
    'version': '0.1.0',
    'description': 'A simple command-line tool that graphs Chess.com game stats',
    'long_description': None,
    'author': 'julianmclain',
    'author_email': 'julianrmclain@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
