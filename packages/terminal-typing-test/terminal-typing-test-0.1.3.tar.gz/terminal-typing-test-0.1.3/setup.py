# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['terminal_typing_test']

package_data = \
{'': ['*'], 'terminal_typing_test': ['text/*', 'text/short/*']}

entry_points = \
{'console_scripts': ['typingtest = terminal_typing_test.main:run']}

setup_kwargs = {
    'name': 'terminal-typing-test',
    'version': '0.1.3',
    'description': 'A terminal-based typing test.',
    'long_description': '# Terminal Typing Test\n\n[![Fawaz Shah](https://circleci.com/gh/fawazshah/terminal-typing-test.svg?style=shield)](https://app.circleci.com/pipelines/github/fawazshah/terminal-typing-test)\n\nFind your typing speed through the command line!\n\nInstall with `pip install terminal-typing-test`. Once installed, run `typingtest` from the command line.\n\n',
    'author': 'Fawaz Shah',
    'author_email': 'fawaz010@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
