# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lint_test']

package_data = \
{'': ['*']}

install_requires = \
['black>=20.8b1,<21.0', 'flake8>=3.8.3,<4.0.0', 'pendulum>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'lint-test',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
