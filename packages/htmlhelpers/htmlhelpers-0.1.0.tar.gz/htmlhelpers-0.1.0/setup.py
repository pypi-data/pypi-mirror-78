# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['htmlhelpers']

package_data = \
{'': ['*']}

install_requires = \
['m2r>=0.2.1,<0.3.0']

setup_kwargs = {
    'name': 'htmlhelpers',
    'version': '0.1.0',
    'description': 'Simple package that helps with creating html strings.',
    'long_description': None,
    'author': 'steventimberman',
    'author_email': 'stevetimberman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
