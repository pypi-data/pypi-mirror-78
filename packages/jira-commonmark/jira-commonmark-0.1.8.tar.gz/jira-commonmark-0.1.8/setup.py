# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jira_commonmark', 'jira_commonmark.handlers']

package_data = \
{'': ['*']}

install_requires = \
['importlib_metadata>=1.7.0,<2.0.0', 'urllib3>=1.25.10,<2.0.0']

setup_kwargs = {
    'name': 'jira-commonmark',
    'version': '0.1.8',
    'description': '',
    'long_description': None,
    'author': 'pbencze',
    'author_email': 'paul@idelab.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
