# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fds', 'fds.auth', 'fds.auth.signature', 'fds.model']

package_data = \
{'': ['*']}

install_requires = \
['argcomplete>=1.9,<2.0',
 'click>=7.0,<8.0',
 'crcmod>=1.7,<2.0',
 'requests>=2.21,<3.0']

extras_require = \
{':python_version >= "2.7" and python_version < "2.8"': ['pathlib2>=2.2,<3.0',
                                                         'futures'],
 ':python_version >= "3.4" and python_version < "3.5"': ['enum34']}

entry_points = \
{'console_scripts': ['fds = fds.fds_cli:main', 'fdscli = fds.fdscli_cli:main']}

setup_kwargs = {
    'name': 'galaxy-fds-sdk',
    'version': '1.4.37',
    'description': 'Python sdk for Galaxy FDS',
    'long_description': None,
    'author': 'hujianxin',
    'author_email': 'hujianxin@xiaomi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
