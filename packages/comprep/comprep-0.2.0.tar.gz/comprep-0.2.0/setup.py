# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['comprep']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.3,<0.5.0']

setup_kwargs = {
    'name': 'comprep',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'riku.okajima',
    'author_email': 'riku.okajima@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
