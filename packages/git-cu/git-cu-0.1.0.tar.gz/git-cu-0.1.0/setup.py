# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_cu']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['git-cu = gitcu.main:main']}

setup_kwargs = {
    'name': 'git-cu',
    'version': '0.1.0',
    'description': 'Helps organize git repositories by cloning into a directory structure based on the URL',
    'long_description': None,
    'author': 'Vasili Revelas',
    'author_email': 'vasili.revelas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
