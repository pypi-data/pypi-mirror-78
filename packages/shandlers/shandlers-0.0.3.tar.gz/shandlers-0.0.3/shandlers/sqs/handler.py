import json
from json import JSONDecodeError

from marshmallow.exceptions import ValidationError

from shandlers.logger import create_logger
from shandlers.sqs.exceptions import SQSHandlerError
from shandlers.sqs.schema import SQSEventSchema

_SQS_EVENT_SCHEMA = SQSEventSchema()
_LOGGER = create_logger()


def sqs_handler(schema=json, retry_threshold=1, logger=_LOGGER):
    if retry_threshold <= 0:
        raise ValueError("The retry_threshold must be a positive non-null value")

    def handler_factory(func):
        return _SQSHandler(func, schema, retry_threshold, logger).handle

    return handler_factory


class _SQSHandler:

    def __init__(self, func, schema, retry_threshold, logger):
        self.func = func
        self.schema = schema
        self.retry_threshold = retry_threshold
        self.logger = logger

    def handle(self, event, context):

        try:
            sqs_event = _SQS_EVENT_SCHEMA.load(event)

            for record in sqs_event:

                receive_count = int(record.receive_count)
                if receive_count <= self.retry_threshold:
                    payload = self.schema.loads(record.body)
                    self.func(payload=payload, receive_count=receive_count, event=sqs_event)
                else:
                    self.logger.warning(
                        f"Message exceeded the retry threshold ({self.retry_threshold}). "
                        f"MessageID: {record.message_id}"
                    )

        except (ValidationError, JSONDecodeError) as err:
            self.logger.error(f"Error while parsing: {err}. Event discarded.")
        except Exception as err:
            self.logger.exception(f"Error while processing. Event discarded.")
            raise SQSHandlerError() from err
