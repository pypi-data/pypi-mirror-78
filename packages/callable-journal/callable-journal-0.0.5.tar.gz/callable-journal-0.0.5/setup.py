# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['callable_journal']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.6.1,<2.0.0', 'pyyaml>=5.3.1,<6.0.0', 'toolz>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'callable-journal',
    'version': '0.0.5',
    'description': 'Log message generator for callables argument and return values.',
    'long_description': '# callable-journal\n[![CI](https://github.com/nathan5280/callable-journal/workflows/Test/badge.svg)](https://github.com/nathan5280/callable-journal/actions)\n[![coverage](https://codecov.io/gh/nathan5280/callable-journal/develop/graph/badge.svg)](https://codecov.io/gh/nathan5280/callable-journal)\n[![pypi](https://img.shields.io/pypi/v/callable-journal.svg)](https://pypi.python.org/pypi/callable-journal)\n[![versions](https://img.shields.io/pypi/pyversions/callable-journal.svg)](https://github.com/nathan5280/callable-journal)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/nathan5280/callable-journal/blob/master/LICENSE)\n\nLog message generator for callables argument and return values.',
    'author': 'Nate Atkins',
    'author_email': 'atkinsnw@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nathan5280/ndl-tools',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
