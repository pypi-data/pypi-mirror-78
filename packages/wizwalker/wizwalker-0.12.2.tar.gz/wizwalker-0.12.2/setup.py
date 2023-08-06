# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wizwalker',
 'wizwalker.cli',
 'wizwalker.combat',
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
    'version': '0.12.2',
    'description': 'Automation bot for wizard101',
    'long_description': "# In development\n# WizWalker\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nWizard101 quest bot scripting api and application\n\n## documentation\nyou can find the documentation [here](https://starrfox.github.io/wizwalker/)\n\nyou can download these from the gh-pages branch if desired\n\n## install\ndownload latest release from [here](https://github.com/StarrFox/WizWalker/releases)\nor install from pypi `pip install -U wizwalker`\n\n## discord\njoin the offical discord [here](https://discord.gg/JHrdCNK)\n\n## development install\nThis package uses [poetry](https://python-poetry.org/)\n```shell script\n$ poetry install\n```\n\n## running\nShell may need admin perms\n```shell script\n$ poetry shell\n$ py -m wizwalker\n```\n\n## building\nYou'll need the dev install (see above) for this to work\n\n### exe\n```shell script\n# Admin if needed\n$ pyinstaller -F --uac-admin --name WizWalker wizwalker/__main__.py\n# Normal\n$ pyinstaller -F --name WizWalker wizwalker/__main__.py\n```\n\n### wheel and source\n```shell script\n$ poetry build\n```\n\n### Docs\n```shell script\n$ cd docs\n$ make html\n```\n\n## console commands\nwizwalker: Runs the wizwalker bot\n\nwiz: Starts a Wizard101 instance\n\n## project goals in order of importance\n0. ~~basic info by memory~~\n1. able to determine current quest\n2. ~~teleportion mode~~\n3. ~~info by memory~~\n4. ~~info by packet~~\n5. ~~able to walk~~\n6. able to combat\n7. ~~cli for end users~~\n8. gui for end users\n",
    'author': 'StarrFox',
    'author_email': 'starrfox6312@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/StarrFox/wizwalker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
