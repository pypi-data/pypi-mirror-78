# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moodlepy',
 'moodlepy.base',
 'moodlepy.core',
 'moodlepy.mod',
 'moodlepy.mod.forum',
 'moodlepy.utils']

package_data = \
{'': ['*']}

install_requires = \
['dacite>=1.5.1,<2.0.0', 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'moodlepy',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'hexatester',
    'author_email': 'habibrohman@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
