# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['phantoms']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'phantoms',
    'version': '0.0.1',
    'description': 'Declarative and type-safe domain validation.',
    'long_description': '# phantoms\n\nDeclarative and type-safe domain validation.\n',
    'author': 'sobolevn',
    'author_email': 'mail@sobolevn.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://phantoms.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
