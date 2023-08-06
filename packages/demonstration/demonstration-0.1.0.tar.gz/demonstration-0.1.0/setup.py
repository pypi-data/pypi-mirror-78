# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['demonstration']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'demonstration',
    'version': '0.1.0',
    'description': 'Demo package for learning Python development',
    'long_description': '# python-package-template\nTemplate repository for creating Python packages with GitHub\n',
    'author': 'Akio Taniguchi',
    'author_email': 'taniguchi@a.phys.nagoya-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/astropenguin/python-package-template/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
