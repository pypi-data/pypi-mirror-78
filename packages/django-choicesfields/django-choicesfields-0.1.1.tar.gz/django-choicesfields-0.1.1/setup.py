# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['choicesfields']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.0.0']

setup_kwargs = {
    'name': 'django-choicesfields',
    'version': '0.1.1',
    'description': 'Django fields for modern choices',
    'long_description': None,
    'author': 'Alexander Viklund',
    'author_email': 'bullfest@sthlm.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
