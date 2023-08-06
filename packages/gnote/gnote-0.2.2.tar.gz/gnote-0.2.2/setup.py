# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gnote']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'configparser>=5.0.0,<6.0.0',
 'gitpython>=3.1.7,<4.0.0',
 'loguru>=0.5.1,<0.6.0',
 'rich==5.1.2',
 'toml>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['gnote = gnote.cli:entry']}

setup_kwargs = {
    'name': 'gnote',
    'version': '0.2.2',
    'description': 'code note book',
    'long_description': None,
    'author': 'guojian',
    'author_email': 'guojian_k@qq.com',
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
