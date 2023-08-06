# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logtron',
 'logtron.config',
 'logtron.formatters',
 'logtron.handlers',
 'logtron.util']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=1.7.0,<2.0.0', 'pyyaml>=5.3.1,<6.0.0']

setup_kwargs = {
    'name': 'logtron',
    'version': '0.1.10',
    'description': 'A simple logging library with JSON log formatting',
    'long_description': '# Logtron\n\n[![Release](https://img.shields.io/pypi/v/logtron?logo=python&style=flat)](https://pypi.org/project/logtron)\n[![Downloads](https://img.shields.io/pypi/dm/logtron?logo=python&style=flat)](https://pypi.org/project/logtron)\n[![Supported Versions](https://img.shields.io/pypi/pyversions/logtron.svg?logo=python&style=flat)](https://pypi.org/project/logtron)\n[![License](https://img.shields.io/github/license/ilija1/logtron?logo=apache&style=flat)](LICENSE)\n\n[![Build](https://img.shields.io/travis/ilija1/logtron?logo=travis&style=flat)](https://travis-ci.org/ilija1/logtron)\n[![Coverage](https://img.shields.io/codecov/c/gh/ilija1/logtron?logo=codecov&style=flat)](https://codecov.io/gh/ilija1/logtron)\n[![Documentation](https://img.shields.io/readthedocs/logtron?logo=read-the-docs&style=flat)](https://logtron.readthedocs.io/en/latest)\n[![Maintainability](https://img.shields.io/codeclimate/maintainability/ilija1/logtron?logo=code-climate&style=flat)](https://codeclimate.com/github/ilija1/logtron/maintainability)\n[![Tech Debt](https://img.shields.io/codeclimate/tech-debt/ilija1/logtron?logo=code-climate&style=flat)](https://codeclimate.com/github/ilija1/logtron/issues)\n[![Issues](https://img.shields.io/codeclimate/issues/ilija1/logtron?logo=code-climate&style=flat)](https://codeclimate.com/github/ilija1/logtron/issues)\n\n**Logtron** is a simple logging library with JSON log formatting.\n\n```python\n>>> import logtron\n>>> logger = logtron.autodiscover()\n>>> logger.info("hello world")\n{"timestamp": 1598900664859, "message": "hello world", "name": "root", "level": 20, "context": {}, "extra": {}}\n>>> logger.info("extra args", extra={"foo": "bar", "count": 7})\n{"timestamp": 1598900667704, "message": "extra args", "name": "root", "level": 20, "context": {}, "extra": {"foo": "bar", "count": 7}}\n>>>\n```\n\nOr\n\n```python\n>>> import logtron\n>>> logtron.autodiscover() # Only needs to run once somewhere to configure the root logger\n<RootLogger root (INFO)>\n>>>\n>>> import logging\n>>> logger = logging.getLogger()\n>>> logger.info("hello world")\n{"timestamp": 1598900735699, "message": "hello world", "name": "root", "level": 20, "context": {}, "extra": {}}\n>>> logger.info("extra args", extra={"foo": "bar", "count": 7})\n{"timestamp": 1598900757238, "message": "extra args", "name": "root", "level": 20, "context": {}, "extra": {"foo": "bar", "count": 7}}\n>>>\n```\n\nLogtron allows you to skip all the usual boilerplate when configuring python logging.\n\nLogtron will default to a console JSON log formatter that is compatible with popular log aggregators such as [Logstash](https://www.elastic.co/guide/en/logstash/current/introduction.html), [Fluent Bit](https://docs.fluentbit.io/manual/), or [AWS CloudWatch Logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html).\n\n## Installing Logtron and Supported Versions\n\nLogtron is available on PyPI:\n\n```shell\n$ python -m pip install logtron\n```\n\nLogtron officially supports Python 2.7 & 3.5+.\n',
    'author': 'Ilija Stevcev',
    'author_email': 'ilija1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ilija1/logtron/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
