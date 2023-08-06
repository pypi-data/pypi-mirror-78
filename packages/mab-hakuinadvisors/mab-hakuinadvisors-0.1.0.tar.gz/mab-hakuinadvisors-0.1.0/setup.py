# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mab-hakuinadvisors']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mab-hakuinadvisors',
    'version': '0.1.0',
    'description': 'Multiarm bandit solutions',
    'long_description': None,
    'author': 'Alexey',
    'author_email': 'butirev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
