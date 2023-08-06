# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['innvariant', 'innvariant.networkx']

package_data = \
{'': ['*']}

extras_require = \
{'all': ['networkx>=2.5,<3.0'], 'networkx': ['networkx>=2.5,<3.0']}

setup_kwargs = {
    'name': 'innvariant',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Julian Stier',
    'author_email': 'julian.stier@uni-passau.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
