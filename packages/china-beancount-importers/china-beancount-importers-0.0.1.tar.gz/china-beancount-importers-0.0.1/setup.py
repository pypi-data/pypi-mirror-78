# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['china_beancount_importers']

package_data = \
{'': ['*']}

install_requires = \
['beancount>=2.3.0,<3.0.0,!=2.3.1']

setup_kwargs = {
    'name': 'china-beancount-importers',
    'version': '0.0.1',
    'description': 'A set of importers maybe useful for you in China.',
    'long_description': None,
    'author': 'Trim21',
    'author_email': 'i@trim21.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Trim21/china-beancount-importers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
