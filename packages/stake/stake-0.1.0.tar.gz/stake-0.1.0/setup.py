# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stake']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0',
 'inflection>=0.5.0,<0.6.0',
 'pydantic>=1.5.1,<2.0.0',
 'python-dotenv>=0.13.0,<0.14.0']

setup_kwargs = {
    'name': 'stake',
    'version': '0.1.0',
    'description': 'stake.com.au unofficial api',
    'long_description': None,
    'author': 'Stefano Tabacco',
    'author_email': 'tabacco.stefano@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
