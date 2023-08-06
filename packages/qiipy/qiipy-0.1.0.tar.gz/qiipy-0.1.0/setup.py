# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qiipy']

package_data = \
{'': ['*']}

install_requires = \
['apywrapper>=0.1.4,<0.2.0']

setup_kwargs = {
    'name': 'qiipy',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'sh1ma',
    'author_email': 'in9lude@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
