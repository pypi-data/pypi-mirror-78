# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['nulltype']

package_data = \
{'': ['*']}

install_requires = \
['keats>=0.2.28,<0.3.0']

setup_kwargs = {
    'name': 'jdv-nulltype',
    'version': '1.0.0',
    'description': 'Just a singleton Null object (i.e. `Null is not None`)',
    'long_description': None,
    'author': 'Justin Vrana',
    'author_email': 'justin.vrana@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
