# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['terminal_typing_test']

package_data = \
{'': ['*'], 'terminal_typing_test': ['text/*']}

entry_points = \
{'console_scripts': ['typingtest = terminal_typing_test.main:run']}

setup_kwargs = {
    'name': 'terminal-typing-test',
    'version': '0.1.1',
    'description': 'A Terminal-based typing test.',
    'long_description': '# Terminal Typing Test\n\nFind your typing speed through the command line!\n\nInstall with `pip install terminal-typing-test`. Once installed, run `typingtest` from the command line.\n\n',
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
