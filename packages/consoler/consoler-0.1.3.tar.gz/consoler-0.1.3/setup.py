# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['consoler']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.15.5,<0.16.0', 'loguru>=0.4.1']

setup_kwargs = {
    'name': 'consoler',
    'version': '0.1.3',
    'description': '',
    'long_description': '## Consoler\n\nA terminal printer that\'s totally tailored to how I like terminal printouts. If this happens to also be how you like terminal printouts, this package may well be for you too.\n\n### Installing\n\n`poetry add consoler` or `pip install consoler`\n\n### Usage\n\n    from consoler import console\n    console.log("This is a log level print out")\n    console.info("This is an info level print out")\n    console.warn("This is a warning level print out")\n\n    try:\n        1 / 0\n    except Exception as e:\n        console.error("Oh no!", e)\n\n\n### Settings\n\nUsing with Django you set a few things in the Django settings to affect behaviour of conoler.\n\n    DEBUG = True\n\nIf `DEBUG` is `True` consoler will print to stdout, otherwise it will send the output to loguru.\n\n    CONSOLE_LOG_LEVEL = \'LOG\'\n\nYou can set a log level for which message you want to reach the screen. Available levels are...\n\n    LOG\n    INFO\n    SUCCESS\n    TEMPLATE\n    WARN\n    ERROR\n\n    CONSOLE_PATH_PREFIX = \'\'\n\nWhen developing in a docker container or VM, the start of consoler\'s file paths might not quite match your local filesystem. Set a prefix here to prepend to the output\'s path string. This is super useful if you use https://github.com/dandavison/iterm2-dwim to make file paths clickable in iTerm.\n',
    'author': 'Hactar',
    'author_email': 'systems@hactar.is',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hactar-is/consoler',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
