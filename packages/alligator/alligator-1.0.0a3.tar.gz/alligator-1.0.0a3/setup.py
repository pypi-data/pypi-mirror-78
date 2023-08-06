# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alligator', 'alligator.backends']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'alligator',
    'version': '1.0.0a3',
    'description': 'Simple offline task queues.',
    'long_description': None,
    'author': 'Daniel Lindsley',
    'author_email': 'daniel@toastdriven.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
