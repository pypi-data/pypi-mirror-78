# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gdict']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'lxml>=4.5.2,<5.0.0', 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['gdict = gdict.cli:entry']}

setup_kwargs = {
    'name': 'gdict',
    'version': '0.1.1',
    'description': '',
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
