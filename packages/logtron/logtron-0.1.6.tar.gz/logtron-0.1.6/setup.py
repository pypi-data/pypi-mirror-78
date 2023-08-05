# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logtron', 'logtron.config', 'logtron.formatters', 'logtron.handlers']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=1.7.0,<2.0.0', 'pyyaml>=5.3.1,<6.0.0']

setup_kwargs = {
    'name': 'logtron',
    'version': '0.1.6',
    'description': 'A simple logging library with JSON log formatting',
    'long_description': '# Logtron\n\n**Logtron** is a simple logging library with JSON log formatting.\n\n```python\n>>> import logtron\n>>> logger = logtron.autodiscover()\n>>> logger.info("hello world")\n{"timestamp": 1598900664859, "message": "hello world", "name": "root", "level": 20, "context": {}, "extra": {}}\n>>> logger.info("extra args", extra={"foo": "bar", "count": 7})\n{"timestamp": 1598900667704, "message": "extra args", "name": "root", "level": 20, "context": {}, "extra": {"foo": "bar", "count": 7}}\n>>>\n```\n\nOr\n\n```python\n>>> import logtron\n>>> logtron.autodiscover() # Only needs to run once somewhere to configure the root logger\n<RootLogger root (INFO)>\n>>>\n>>> import logging\n>>> logger = logging.getLogger()\n>>> logger.info("hello world")\n{"timestamp": 1598900735699, "message": "hello world", "name": "root", "level": 20, "context": {}, "extra": {}}\n>>> logger.info("extra args", extra={"foo": "bar", "count": 7})\n{"timestamp": 1598900757238, "message": "extra args", "name": "root", "level": 20, "context": {}, "extra": {"foo": "bar", "count": 7}}\n>>>\n```\n\nLogtron allows you to skip all the usual boilerplate when configuring python logging.\n\nLogtron will default to a console JSON log formatter that is compatible with popular log aggregators such as [Logstash](https://www.elastic.co/guide/en/logstash/current/introduction.html), [Fluent Bit](https://docs.fluentbit.io/manual/), or [AWS CloudWatch Logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html).\n\n[![Downloads](https://pepy.tech/badge/logtron/month)](https://pepy.tech/project/logtron/month)\n[![Supported Versions](https://img.shields.io/pypi/pyversions/logtron.svg)](https://pypi.org/project/logtron)\n[![Contributors](https://img.shields.io/github/contributors/ilija1/logtron.svg)](https://github.com/ilija1/logtron/graphs/contributors)\n\n[![Build Status](https://travis-ci.org/ilija1/logtron.svg?branch=master)](https://travis-ci.org/ilija1/logtron)\n[![codecov](https://codecov.io/gh/ilija1/logtron/branch/master/graph/badge.svg)](https://codecov.io/gh/ilija1/logtron)\n[![Documentation Status](https://readthedocs.org/projects/logtron/badge/?version=latest)](https://logtron.readthedocs.io/en/latest/?badge=latest)\n\n## Installing Logtron and Supported Versions\n\nLogtron is available on PyPI:\n\n```shell\n$ python -m pip install logtron\n```\n\nLogtron officially supports Python 2.7 & 3.5+.\n',
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
