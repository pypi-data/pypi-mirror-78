# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['huehue', 'huehue.bridge', 'huehue.models']

package_data = \
{'': ['*']}

install_requires = \
['click-log>=0.3.2,<0.4.0',
 'click>=7.1.2,<8.0.0',
 'python-decouple>=3.3,<4.0',
 'urllib3>=1.25.9,<2.0.0']

entry_points = \
{'console_scripts': ['huehue = huehue.cli:cli']}

setup_kwargs = {
    'name': 'huehue',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jay Looney',
    'author_email': 'jay.m.looney@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
