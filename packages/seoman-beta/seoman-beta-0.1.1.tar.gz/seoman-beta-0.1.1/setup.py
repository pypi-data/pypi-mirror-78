# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seoman_beta', 'seoman_beta.utils']

package_data = \
{'': ['*']}

install_requires = \
['google-api-python-client>=1.10.1,<2.0.0',
 'google-auth-oauthlib>=0.4.1,<0.5.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['seoman = seoman_beta.main:app']}

setup_kwargs = {
    'name': 'seoman-beta',
    'version': '0.1.1',
    'description': 'Beta version for seoman',
    'long_description': None,
    'author': 'ycd',
    'author_email': 'yagizcanilbey1903@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ycd/seoman-beta',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
