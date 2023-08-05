# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wizwalker',
 'wizwalker.cli',
 'wizwalker.packets',
 'wizwalker.windows',
 'wizwalker.windows.memory']

package_data = \
{'': ['*']}

install_requires = \
['aioconsole>=0.2.1,<0.3.0',
 'aiofiles>=0.5.0,<0.6.0',
 'appdirs>=1.4.4,<2.0.0',
 'loguru>=0.5.1,<0.6.0',
 'pymem==1.3']

entry_points = \
{'console_scripts': ['wiz = wizwalker.__main__:wiz_command',
                     'wizwalker = wizwalker.__main__:main']}

setup_kwargs = {
    'name': 'wizwalker',
    'version': '0.11.0',
    'description': 'Automation bot for wizard101',
    'long_description': None,
    'author': 'StarrFox',
    'author_email': 'starrfox6312@gmail.com',
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
