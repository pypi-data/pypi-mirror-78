from dataclasses import dataclass

from marshmallow import EXCLUDE, Schema, fields, post_load

# Schemas


class SQSEventAttributesSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    approximate_receive_count = fields.Str(required=True, data_key="ApproximateReceiveCount")
    sent_timestamp = fields.Str(required=True, data_key="SentTimestamp")
    sender_id = fields.Str(required=True, data_key="SenderId")
    approximate_first_receive_timestamp = fields.Str(required=True, data_key="ApproximateFirstReceiveTimestamp")

    @post_load
    def create_sqs_event_attributes(self, data, **_):
        return SQSEventAttributes(**data)


class SQSRecordSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    message_id = fields.Str(required=True, data_key="messageId")
    receipt_handle = fields.Str(required=True, data_key="receiptHandle")
    body = fields.Str(required=True, data_key="body")
    attributes = fields.Nested(SQSEventAttributesSchema, required=True, data_key="attributes")
    message_attributes = fields.Dict(required=True, data_key="messageAttributes")
    md5_of_body = fields.Str(required=True, data_key="md5OfBody")
    event_source = fields.Str(required=True, data_key="eventSource")
    event_source_arn = fields.Str(required=True, data_key="eventSourceARN")
    aws_region = fields.Str(required=True, data_key="awsRegion")

    @post_load
    def create_sqs_record(self, data, **_):
        return SQSRecord(**data)


class SQSEventSchema(Schema):
    records = fields.List(fields.Nested(SQSRecordSchema), data_key="Records")

    @post_load
    def create_sqs_event(self, data, **kwargs):
        return SQSEvent(**data)


# Classes


@dataclass
class SQSEventAttributes(Schema):
    approximate_receive_count: str
    sent_timestamp: str
    sender_id: str
    approximate_first_receive_timestamp: str


@dataclass
class SQSRecord(Schema):
    message_id: str
    receipt_handle: str
    body: str
    attributes: SQSEventAttributes
    message_attributes: dict
    md5_of_body: str
    event_source: str
    event_source_arn: str
    aws_region: str

    @property
    def receive_count(self):
        return self.attributes.approximate_receive_count


@dataclass
class SQSEvent(Schema):
    records: list

    def __iter__(self):
        return iter(self.records)
