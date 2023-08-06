# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logtron_aws', 'logtron_aws.util']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1,<2', 'importlib_metadata>=1.7.0,<2.0.0', 'logtron']

setup_kwargs = {
    'name': 'logtron-aws',
    'version': '0.1.12',
    'description': 'AWS CloudWatch logging and context auto-discovery for logtron',
    'long_description': '# Logtron-AWS\n\n[![Release](https://img.shields.io/pypi/v/logtron-aws?logo=python&style=flat)](https://pypi.org/project/logtron-aws)\n[![Downloads](https://img.shields.io/pypi/dm/logtron-aws?logo=python&style=flat)](https://pypi.org/project/logtron-aws)\n[![Supported Versions](https://img.shields.io/pypi/pyversions/logtron-aws.svg?logo=python&style=flat)](https://pypi.org/project/logtron-aws)\n[![License](https://img.shields.io/github/license/ilija1/logtron-aws?logo=apache&style=flat)](LICENSE)\n\n[![Build](https://img.shields.io/travis/ilija1/logtron-aws?logo=travis&style=flat)](https://travis-ci.org/ilija1/logtron-aws)\n[![Coverage](https://img.shields.io/codecov/c/gh/ilija1/logtron-aws?logo=codecov&style=flat)](https://codecov.io/gh/ilija1/logtron-aws)\n[![Documentation](https://img.shields.io/readthedocs/logtron-aws?logo=read-the-docs&style=flat)](https://logtron-aws.readthedocs.io/en/latest)\n[![Maintainability](https://img.shields.io/codeclimate/maintainability/ilija1/logtron-aws?logo=code-climate&style=flat)](https://codeclimate.com/github/ilija1/logtron-aws/maintainability)\n[![Tech Debt](https://img.shields.io/codeclimate/tech-debt/ilija1/logtron-aws?logo=code-climate&style=flat)](https://codeclimate.com/github/ilija1/logtron-aws/issues)\n[![Issues](https://img.shields.io/codeclimate/issues/ilija1/logtron-aws?logo=code-climate&style=flat)](https://codeclimate.com/github/ilija1/logtron-aws/issues)\n\n**Logtron-AWS** is a set of AWS-targeted extensions for the [**Logtron**](https://github.com/ilija1/logtron) library.\n\n```python\nimport logtron_aws\nlogger = logtron_aws.autodiscover()\nlogger.info("hello world")\n```\n\nOr\n\n```python\nimport logtron_aws\nlogtron_aws.autodiscover() # Only needs to run once somewhere to configure the root logger\n\nimport logging\nlogger = logging.getLogger()\nlogger.info("hello world")\n```\n\nLogtron-AWS provides a set of extensions for the [Logtron](https://github.com/ilija1/logtron) library to enable features such as:\n\n- Automated log context discovery using AWS STS\n- Log handler for logging directly to CloudWatch Logs\n  - Automatic log group creation\n  - Convention-based log group naming derived from IAM role name\n  - Configurable log retention period\n  - Automated background log batch submission to support high frequency logging\n  - Configureable batch submission time interval\n- Highly configurable if needed, but has sane defaults out-of-the-box\n\n## Installing Logtron-AWS and Supported Versions\n\nLogtron-AWS is available on PyPI:\n\n```shell\n$ python -m pip install logtron-aws\n```\n\nLogtron-AWS officially supports Python 2.7 & 3.5+.\n',
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
