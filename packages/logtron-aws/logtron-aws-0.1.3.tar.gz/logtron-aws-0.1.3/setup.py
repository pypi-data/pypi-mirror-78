# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logtron_aws']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.14.51,<2.0.0',
 'importlib_metadata>=1.7.0,<2.0.0',
 'logtron>=0.1.3,<0.2.0']

setup_kwargs = {
    'name': 'logtron-aws',
    'version': '0.1.3',
    'description': 'AWS CloudWatch logging and context auto-discovery for logtron',
    'long_description': '# Logtron-AWS\n\n**Logtron-AWS** is a set of AWS-targeted extensions for the **Logtron** library.\n\n```python\nimport logtron_aws\nlogger = logtron_aws.autodiscover()\nlogger.info("hello world")\n```\n\nOr\n\n```python\nimport logtron_aws\nlogtron_aws.autodiscover() # Only needs to run once somewhere to configure the root logger\n\nimport logging\nlogger = logging.getLogger()\nlogger.info("hello world")\n```\n\nLogtron-AWS provides a set of extensions for the [Logtron](https://github.com/ilija1/logtron/) library to enable features such as:\n\n- Automated log context discovery using AWS STS\n- Log handler for logging directly to CloudWatch Logs\n\n[![Downloads](https://pepy.tech/badge/logtron-aws/month)](https://pepy.tech/project/logtron-aws/month)\n[![Supported Versions](https://img.shields.io/pypi/pyversions/logtron-aws.svg)](https://pypi.org/project/logtron-aws)\n[![Contributors](https://img.shields.io/github/contributors/ilija1/logtron-aws.svg)](https://github.com/ilija1/logtron-aws/graphs/contributors)\n\n## Installing Logtron-AWS and Supported Versions\n\nLogtron-AWS is available on PyPI:\n\n```shell\n$ python -m pip install logtron-aws\n```\n\nLogtron-AWS officially supports Python 2.7 & 3.5+.\n',
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
