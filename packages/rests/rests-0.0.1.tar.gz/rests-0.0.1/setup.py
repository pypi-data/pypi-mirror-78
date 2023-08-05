# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rests',
    'version': '0.0.1',
    'description': 'Framework independent REST the way it should be! ',
    'long_description': '# rests\nFramework independent REST the way it should be!\n',
    'author': 'sobolevn',
    'author_email': 'mail@sobolevn.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://rests.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
