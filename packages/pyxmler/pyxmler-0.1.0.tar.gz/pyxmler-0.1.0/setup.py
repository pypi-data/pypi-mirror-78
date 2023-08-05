# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyxmler']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyxmler',
    'version': '0.1.0',
    'description': 'Converts a Python dictionary into a valid XML string',
    'long_description': None,
    'author': 'Ramiro Tician',
    'author_email': 'ramirotician@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
