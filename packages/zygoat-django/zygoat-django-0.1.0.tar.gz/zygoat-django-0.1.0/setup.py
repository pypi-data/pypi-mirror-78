# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zygoat_django']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.1.1,<4.0.0', 'importlib-metadata>=1.7.0,<2.0.0']

setup_kwargs = {
    'name': 'zygoat-django',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Mark Rawls',
    'author_email': 'markrawls96@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
