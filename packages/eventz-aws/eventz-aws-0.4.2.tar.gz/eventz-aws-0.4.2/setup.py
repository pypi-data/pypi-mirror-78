# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eventz_aws']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.14.16,<2.0.0', 'eventz>=0.3.0,<0.4.0', 'immutables>=0.14,<0.15']

setup_kwargs = {
    'name': 'eventz-aws',
    'version': '0.4.2',
    'description': 'AWS additions for Eventz framework.',
    'long_description': None,
    'author': 'Dan Ballance',
    'author_email': 'work@danballance.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
