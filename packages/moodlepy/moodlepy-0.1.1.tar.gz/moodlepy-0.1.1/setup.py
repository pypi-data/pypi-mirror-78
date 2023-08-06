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

entry_points = \
{'console_scripts': ['moodlepy = moodlepy.__main__:main']}

setup_kwargs = {
    'name': 'moodlepy',
    'version': '0.1.1',
    'description': 'Client for moodle webservice',
    'long_description': '# moodlepy\n\n[![moodlepy - PyPi](https://img.shields.io/pypi/v/moodlepy)](https://pypi.org/project/moodlepy/)\n[![codecov](https://codecov.io/gh/hexatester/moodlepy/branch/master/graph/badge.svg)](https://codecov.io/gh/hexatester/moodlepy)\n[![BUILD](https://img.shields.io/travis/com/hexatester/moodlepy)](https://travis-ci.com/github/hexatester/moodlepy)\n[![LICENSE](https://img.shields.io/github/license/hexatester/moodlepy)](https://github.com/hexatester/moodlepy/blob/master/LICENSE)\n\nPython client for moodle webservice\n',
    'author': 'hexatester',
    'author_email': 'habibrohman@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hexatester/moodlepy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
