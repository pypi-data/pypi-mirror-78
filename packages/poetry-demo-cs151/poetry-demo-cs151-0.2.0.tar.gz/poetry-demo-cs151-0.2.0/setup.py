# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_demo_cs151']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'poetry-demo-cs151',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Craig Saxton',
    'author_email': 'csaxton171@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
