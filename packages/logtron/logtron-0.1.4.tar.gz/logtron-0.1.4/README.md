# Logtron

**Logtron** is a simple logging library with JSON log formatting.

```python
import logtron
logger = logtron.autodiscover()
logger.info("hello world")
```

Or

```python
import logtron
logtron.autodiscover() # Only needs to run once somewhere to configure the root logger

import logging
logger = logging.getLogger()
logger.info("hello world")
```

Logtron allows you to skip all the usual boilerplate when configuring python logging.

Logtron will default to a console JSON log formatter that is compatible with popular log aggregators such as [Logstash](https://www.elastic.co/guide/en/logstash/current/introduction.html), [Fluent Bit](https://docs.fluentbit.io/manual/), or [AWS CloudWatch Logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html).

[![Downloads](https://pepy.tech/badge/logtron/month)](https://pepy.tech/project/logtron/month)
[![Supported Versions](https://img.shields.io/pypi/pyversions/logtron.svg)](https://pypi.org/project/logtron)
[![Contributors](https://img.shields.io/github/contributors/ilija1/logtron.svg)](https://github.com/ilija1/logtron/graphs/contributors)
[![Build Status](https://travis-ci.org/ilija1/logtron.svg?branch=master)](https://travis-ci.org/ilija1/logtron)
[![codecov](https://codecov.io/gh/ilija1/logtron/branch/master/graph/badge.svg)](https://codecov.io/gh/ilija1/logtron)

## Installing Logtron and Supported Versions

Logtron is available on PyPI:

```shell
$ python -m pip install logtron
```

Logtron officially supports Python 2.7 & 3.5+.
