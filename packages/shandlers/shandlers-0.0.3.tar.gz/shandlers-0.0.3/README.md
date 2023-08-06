# shandlers

[![serverless](http://public.serverless.com/badges/v3.svg)](http://www.serverless.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://travis-ci.com/GonzaloSaad/shandlers.svg?branch=master)](https://travis-ci.com/GonzaloSaad/shandlers)

A python lib that provides handlers for serverless events

&nbsp;
## Installation

From PyPI:

    shandlers==0.0.3

&nbsp;
## Supported events
- [x] sqs
- [ ] apigw
- [ ] sns
- [ ] kinesis stream
- [ ] kinesis firehose


&nbsp;
## Basic Usage

### SQS Handler

Create a function that accepts a `payload` and `kwargs` as parameters, that contains the logic
that you want to apply to **each** of your records in the event.

```python
def handle(payload, **kwargs):
    pass
```

Add the `@sqs_handler` decorator to the function

```python
from shandlers.sqs.handler import sqs_handler

@sqs_handler()
def handle(payload, **kwargs):
    pass
```

The decorator will allow your function to:
- Parse the SQS event (using [`marshmallow`](https://github.com/marshmallow-code/marshmallow))
- Parse the `body` of each record to a `dict` and pass it to your function
- Handle a basic retry logic
- Handle `ValidationError` and `JSONDecodeError`

&nbsp;
#### The kwargs argument in your function

You can have extra arguemtns in your function if you need to. The `sqs_handler` decorator
also passes `receive_count` and `event` as parameters, in case you need to perform
extra actions with that information.

```python
from shandlers.sqs.handler import sqs_handler

@sqs_handler()
def handle(payload, receive_count, event, **kwargs):
    pass
```

&nbsp;
#### Configuring the decorator

#### Schema

You can add `schema` to the decorator parameters, in case you have for example
a `marshmallow` schema or if you have any other mechanism to parse that responds to
the `.loads(json_string)` call.

```python
from shandlers.sqs.handler import sqs_handler
from myschema import MyMarshmallowSchema

@sqs_handler(schema=MyMarshmallowSchema())
def handle(payload, **kwargs):
    pass
```

Here the `payload` argument type will depend on the passed schema output.

Also, if while parsing the record `body` a parsing error occurs, the event
will be **DISCARDED**.

> The default value of `schema` is the `json` module from python

#### Retry threshold

You can add `retry_theshold` to the decorator parameters to specify the
amount of times a `record` can retry to be processed.

```python
from shandlers.sqs.handler import sqs_handler

@sqs_handler(retry_threshold=5)
def handle(payload, **kwargs):
    pass
```

> The default value is set to `1`

#### Logger

You can add `logger` to the decorator parameter, so the handlers uses your logger
when an error occurs.

```python
from shandlers.sqs.handler import sqs_handler
import logging

_LOGGER = logging.getLogger()

@sqs_handler(logger=_LOGGER)
def handle(payload, **kwargs):
    pass
```

> The default logger can be checked [here](shandlers/logger.py)
