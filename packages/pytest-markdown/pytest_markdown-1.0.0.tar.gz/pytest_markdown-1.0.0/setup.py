# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_markdown']

package_data = \
{'': ['*']}

install_requires = \
['CommonMark>=0.8.1,<0.9.0', 'pytest>=6.0.1,<7.0.0']

entry_points = \
{'pytest11': ['markdown = pytest_markdown.plugin']}

setup_kwargs = {
    'name': 'pytest-markdown',
    'version': '1.0.0',
    'description': 'Docker integration tests for pytest',
    'long_description': '# pytest-markdown\n\nYou have written a `README.md`. In contains some of your best words. They are in an order, and you are happy its a good order. But all those code blocks... Do they contain valid python? This plugin will find tests in your markdown files and run them.\n',
    'author': 'John Carr',
    'author_email': 'john.carr@unrouted.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Jc2k/pytest-markdown',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
