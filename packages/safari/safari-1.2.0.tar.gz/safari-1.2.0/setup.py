# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['safari']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'safari',
    'version': '1.2.0',
    'description': 'Python utilities for Safari.',
    'long_description': None,
    'author': 'Yevgnen Koh',
    'author_email': 'wherejoystarts@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
