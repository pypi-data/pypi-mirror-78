# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypi_cloud']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pypi-cloud',
    'version': '0.0.0a0',
    'description': 'Host a personal PyPi clone in the cloud.',
    'long_description': '# pypi-cloud\n\nHost a personal PyPi clone in the cloud.\n',
    'author': 'Kyle Finley',
    'author_email': 'kyle@finley.sh',
    'maintainer': None,
    'maintainer_email': None,
    'url': '',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
