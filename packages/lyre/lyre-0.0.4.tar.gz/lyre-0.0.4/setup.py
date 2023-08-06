# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lyre']

package_data = \
{'': ['*']}

install_requires = \
['aeval>=0.1.2,<0.2.0', 'lsp>=0.1.1,<0.2.0', 'trio>=0.16.0,<0.17.0']

entry_points = \
{'console_scripts': ['lyre = lyre.server:main']}

setup_kwargs = {
    'name': 'lyre',
    'version': '0.0.4',
    'description': '',
    'long_description': None,
    'author': 'Chris Chambers',
    'author_email': 'chris@peanutcode.com',
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
