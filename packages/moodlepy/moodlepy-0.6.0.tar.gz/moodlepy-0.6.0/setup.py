# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moodle',
 'moodle.auth',
 'moodle.auth.email',
 'moodle.base',
 'moodle.base.preference',
 'moodle.core',
 'moodle.core.badges',
 'moodle.core.block',
 'moodle.core.blog',
 'moodle.core.calendar',
 'moodle.core.cohort',
 'moodle.core.comment',
 'moodle.core.competency',
 'moodle.core.course',
 'moodle.core.message',
 'moodle.core.user',
 'moodle.core.webservice',
 'moodle.mod',
 'moodle.mod.forum',
 'moodle.tool',
 'moodle.tool.mobile',
 'moodle.utils']

package_data = \
{'': ['*']}

install_requires = \
['dacite>=1.5.1,<2.0.0', 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['moodle = moodle.__main__:main']}

setup_kwargs = {
    'name': 'moodlepy',
    'version': '0.6.0',
    'description': 'Client for moodle webservice',
    'long_description': "# moodlepy\n\n[![moodlepy - PyPi](https://img.shields.io/pypi/v/moodlepy)](https://pypi.org/project/moodlepy/)\n[![codecov](https://codecov.io/gh/hexatester/moodlepy/branch/master/graph/badge.svg)](https://codecov.io/gh/hexatester/moodlepy)\n[![BUILD](https://img.shields.io/travis/com/hexatester/moodlepy)](https://travis-ci.com/github/hexatester/moodlepy)\n[![LICENSE](https://img.shields.io/github/license/hexatester/moodlepy)](https://github.com/hexatester/moodlepy/blob/master/LICENSE)\n\nPython client for moodle webservice\n\n## Introduction\n\nThis library provide a pure Python interface for [Moodle Web Service](https://docs.moodle.org/dev/Web_services). It's compatible with Python versions 3.6+\n\n## Moodle Web Service support\n\nNot all types and methods are supported, since moodlepy is not yet released.\n\n## Installing\n\nYou can install or upgrade moodlepy with:\n\n```bash\npip install moodlepy --upgrade\n```\n\nOr you can install from source with:\n\n```bash\ngit clone https://github.com/hexatester/moodlepy\ncd moodlepy\npython setup.py install\n```\n\n## Usage\n\nExample usage\n\n```python\nfrom moodle import Moodle\nurl = 'https://my.domain/webservice/rest/server.php'\ntoken = 'super secret token'\nmoodle = Moodle(url, token)\nraw_site_info = moodle('core_webservice_get_site_info')\nsite_info = moodle.core.webservice.get_site_info()  # return typed site_info\n\nprint(raw_site_info)\nprint(site_info)\n```\n\nIn the future all [Web service functions](https://docs.moodle.org/dev/Web_service_API_functions) will covered by moodlepy\n",
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
