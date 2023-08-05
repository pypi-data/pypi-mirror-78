# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logtron_aws']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.14.51,<2.0.0', 'logtron>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'logtron-aws',
    'version': '0.1.1',
    'description': 'AWS CloudWatch logging and context auto-discovery for logtron',
    'long_description': '# logtron-aws\n',
    'author': 'Ilija Stevcev',
    'author_email': 'ilija1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ilija1/logtron-aws/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
