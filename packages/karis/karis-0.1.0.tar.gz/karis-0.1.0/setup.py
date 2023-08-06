# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['karis']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['karis = karis.main:main']}

setup_kwargs = {
    'name': 'karis',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Brandon',
    'author_email': 'brandonskerritt51@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
