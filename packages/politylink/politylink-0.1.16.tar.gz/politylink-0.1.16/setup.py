# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['politylink', 'politylink.graphql', 'politylink.helpers']

package_data = \
{'': ['*']}

install_requires = \
['kanjize>=0.1.0,<0.2.0', 'pandas>=1.0.5,<2.0.0', 'sgqlc>=11.0,<12.0']

setup_kwargs = {
    'name': 'politylink',
    'version': '0.1.16',
    'description': '',
    'long_description': None,
    'author': 'Mitsuki Usui',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
