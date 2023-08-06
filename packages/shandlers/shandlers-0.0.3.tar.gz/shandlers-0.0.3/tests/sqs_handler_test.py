import json
import unittest
from dataclasses import dataclass
from logging import Logger
from unittest.mock import Mock, patch

from marshmallow import Schema, fields, post_load

from shandlers.sqs.handler import sqs_handler


class SQSHandlerDecoratorTest(unittest.TestCase):

    def test_sqs_handler_invalid_retry_threshold(self):
        # Given
        retry_threshold = -1

        # When/Then
        with self.assertRaises(ValueError):
            sqs_handler(retry_threshold=retry_threshold)

    @patch("shandlers.sqs.handler._SQSHandler")
    def test_sqs_handler_no_threshold_no_schema_no_logger(self, sqs_handler_cls):
        # Given
        function = Mock()
        retry_threshold = 1

        # When
        handler_factory = sqs_handler()
        handler_factory(function)

        # Then

        # Assert class instantiation
        sqs_handler_cls.assert_called_once()
        call_arg_list = sqs_handler_cls.call_args_list

        self.assertEqual(1, len(call_arg_list))

        for call in call_arg_list:
            args, _ = call

            function_arg = args[0]
            self.assertEqual(function, function_arg)

            schema_arg = args[1]
            self.assertEqual(json, schema_arg)

            retry_threshold_param = args[2]
            self.assertEqual(retry_threshold, retry_threshold_param)

            logger_arg = args[3]
            self.assertTrue(isinstance(logger_arg, Logger))

    @patch("shandlers.sqs.handler._SQSHandler")
    def test_sqs_handler_no_threshold_no_schema_with_logger(self, sqs_handler_cls):
        # Given
        function = Mock()
        logger = Mock()
        retry_threshold = 1

        # When
        handler_factory = sqs_handler(logger=logger)
        handler_factory(function)

        # Then

        # Assert class instantiation
        sqs_handler_cls.assert_called_once()
        call_arg_list = sqs_handler_cls.call_args_list

        self.assertEqual(1, len(call_arg_list))

        for call in call_arg_list:
            args, _ = call

            function_arg = args[0]
            self.assertEqual(function, function_arg)

            schema_arg = args[1]
            self.assertEqual(json, schema_arg)

            retry_threshold_param = args[2]
            self.assertEqual(retry_threshold, retry_threshold_param)

            logger_arg = args[3]
            self.assertEqual(logger, logger_arg)

    @patch("shandlers.sqs.handler._SQSHandler")
    def test_sqs_handler_no_threshold_with_schema_with_logger(self, sqs_handler_cls):
        # Given
        function = Mock()
        logger = Mock()
        schema = Mock()
        retry_threshold = 1

        # When
        handler_factory = sqs_handler(schema=schema, logger=logger)
        handler_factory(function)

        # Then

        # Assert class instantiation
        sqs_handler_cls.assert_called_once()
        call_arg_list = sqs_handler_cls.call_args_list

        self.assertEqual(1, len(call_arg_list))

        for call in call_arg_list:
            args, _ = call

            function_arg = args[0]
            self.assertEqual(function, function_arg)

            schema_arg = args[1]
            self.assertEqual(schema, schema_arg)

            retry_threshold_param = args[2]
            self.assertEqual(retry_threshold, retry_threshold_param)

            logger_arg = args[3]
            self.assertEqual(logger, logger_arg)

    @patch("shandlers.sqs.handler._SQSHandler")
    def test_sqs_handler_with_threshold_with_schema_with_logger(self, sqs_handler_cls):
        # Given
        function = Mock()
        logger = Mock()
        schema = Mock()
        retry_threshold = 10

        # When
        handler_factory = sqs_handler(schema=schema, retry_threshold=retry_threshold, logger=logger)
        handler_factory(function)

        # Then

        # Assert class instantiation
        sqs_handler_cls.assert_called_once()
        call_arg_list = sqs_handler_cls.call_args_list

        self.assertEqual(1, len(call_arg_list))

        for call in call_arg_list:
            args, _ = call

            function_arg = args[0]
            self.assertEqual(function, function_arg)

            schema_arg = args[1]
            self.assertEqual(schema, schema_arg)

            retry_threshold_param = args[2]
            self.assertEqual(retry_threshold, retry_threshold_param)

            logger_arg = args[3]
            self.assertEqual(logger, logger_arg)


class SQSHandler(unittest.TestCase):

    def test_sqs_handler_no_schema(self):
        # Given
        name = "SomeName"
        age = 25

        event_payload = dict(name=name, age=age)

        event = _create_event_with_json(event_payload)
        context = Mock()

        logger = Mock()

        # When/Then
        @sqs_handler(logger=logger)
        def handle(payload, **kwargs):
            self.assertIsInstance(payload, dict)

            payload_name = payload.get("name")
            self.assertEqual(name, payload_name)

            payload_age = payload.get("age")
            self.assertEqual(age, payload_age)

        handle(event, context)

        # Then
        logger.exception.assert_not_called()
        logger.error.assert_not_called()
        logger.warning.assert_not_called()

    def test_sqs_handler_no_schema_decode_error(self):
        # Given
        name = "SomeName"
        age = 25

        event_payload = "{\"attr\":\"value}"

        event = _create_event(event_payload)
        context = Mock()

        logger = Mock()

        # When/Then
        @sqs_handler(logger=logger)
        def handle(payload, **kwargs):
            self.assertIsInstance(payload, dict)

            payload_name = payload.get("name")
            self.assertEqual(name, payload_name)

            payload_age = payload.get("age")
            self.assertEqual(age, payload_age)

        handle(event, context)

        # Then
        logger.exception.assert_not_called()
        logger.error.assert_called_once()
        logger.warning.assert_not_called()

    def test_sqs_handler_no_schema_exception(self):
        # Given
        name = "SomeName"
        age = 25

        event_payload = dict(name=name, age=age)

        event = _create_event_with_json(event_payload)
        context = Mock()

        logger = Mock()

        # When/Then
        @sqs_handler(logger=logger)
        def handle(payload, **kwargs):
            self.assertIsInstance(payload, dict)

            payload_name = payload.get("name")
            self.assertEqual(name, payload_name)

            payload_age = payload.get("age")
            self.assertEqual(age, payload_age)

            raise Exception("Something happened")

        with self.assertRaises(Exception):
            handle(event, context)

        # Then
        logger.exception.assert_called_once()
        logger.error.assert_not_called()
        logger.warning.assert_not_called()

    def test_sqs_handler_no_schema_retry_exceeded(self):
        # Given
        name = "SomeName"
        age = 25
        retry_threshold = 1
        receive_count = retry_threshold + 2

        event_payload = dict(name=name, age=age)

        event = _create_event_with_json(event_payload, receive_count)
        context = Mock()

        logger = Mock()

        # When/Then
        @sqs_handler(retry_threshold=retry_threshold, logger=logger)
        def handle(payload, **kwargs):
            self.assertIsInstance(payload, dict)

            payload_name = payload.get("name")
            self.assertEqual(name, payload_name)

            payload_age = payload.get("age")
            self.assertEqual(age, payload_age)

        handle(event, context)

        # Then
        logger.exception.assert_not_called()
        logger.error.assert_not_called()
        logger.warning.assert_called_once()

    def test_sqs_handler_with_schema(self):
        # Given
        name = "SomeName"
        age = 25

        event_payload = dict(name=name, age=age)

        event = _create_event_with_json(event_payload)
        context = Mock()

        logger = Mock()

        # When/Then
        @sqs_handler(schema=PayloadSchema(), logger=logger)
        def handle(payload, **kwargs):
            self.assertIsInstance(payload, Payload)
            self.assertEqual(name, payload.name)
            self.assertEqual(age, payload.age)

        handle(event, context)

        # Then
        logger.exception.assert_not_called()
        logger.error.assert_not_called()
        logger.warning.assert_not_called()

    def test_sqs_handler_with_schema_validation_error(self):
        # Given
        name = "SomeName"
        age = 25

        event_payload = "{\"attr\":\"value}"

        event = _create_event(event_payload)
        context = Mock()

        logger = Mock()

        # When/Then
        @sqs_handler(schema=PayloadSchema(), logger=logger)
        def handle(payload, **kwargs):
            self.assertIsInstance(payload, Payload)
            self.assertEqual(name, payload.name)
            self.assertEqual(age, payload.age)

        handle(event, context)

        # Then
        logger.exception.assert_not_called()
        logger.error.assert_called_once()
        logger.warning.assert_not_called()

    def test_sqs_handler_with_schema_exception(self):
        # Given
        name = "SomeName"
        age = 25

        event_payload = dict(name=name, age=age)

        event = _create_event_with_json(event_payload)
        context = Mock()

        logger = Mock()

        # When/Then
        @sqs_handler(schema=PayloadSchema(), logger=logger)
        def handle(payload, **kwargs):
            self.assertIsInstance(payload, Payload)
            self.assertEqual(name, payload.name)
            self.assertEqual(age, payload.age)
            raise Exception("Something happened")

        with self.assertRaises(Exception):
            handle(event, context)

        # Then
        logger.exception.assert_called_once()
        logger.error.assert_not_called()
        logger.warning.assert_not_called()

    def test_sqs_handler_with_schema_retry_exceeded(self):
        # Given
        name = "SomeName"
        age = 25
        retry_threshold = 1
        receive_count = retry_threshold + 2

        event_payload = dict(name=name, age=age)

        event = _create_event_with_json(event_payload, receive_count)
        context = Mock()

        logger = Mock()

        # When/Then
        @sqs_handler(schema=PayloadSchema(), retry_threshold=retry_threshold, logger=logger)
        def handle(payload, **kwargs):
            self.assertIsInstance(payload, Payload)
            self.assertEqual(name, payload.name)
            self.assertEqual(age, payload.age)

        handle(event, context)

        # Then
        logger.exception.assert_not_called()
        logger.error.assert_not_called()
        logger.warning.assert_called_once()


def _create_event_with_json(json_body, receive_count=1):
    return _create_event(json.dumps(json_body), receive_count)


def _create_event(body, receive_count=1):
    return {
        "Records":
            [
                {
                    "messageId": "19dd0b57-b21e-4ac1-bd88-01bbb068cb78",
                    "receiptHandle": "MessageReceiptHandle",
                    "body": body,
                    "attributes":
                        {
                            "ApproximateReceiveCount": str(receive_count),
                            "SentTimestamp": "1523232000000",
                            "SenderId": "123456789012",
                            "ApproximateFirstReceiveTimestamp": "1523232000001"
                        },
                    "messageAttributes": {},
                    "md5OfBody": "7b270e59b47ff90a553787216d55d91d",
                    "eventSource": "aws:sqs",
                    "eventSourceARN": "arn:aws:sqs:us-east-1:123456789012:MyQueue",
                    "awsRegion": "us-east-1"
                }
            ]
    }


class PayloadSchema(Schema):
    name = fields.Str(required=True)
    age = fields.Int(required=True)

    @post_load
    def create_payload(self, data, **kwargs):
        return Payload(**data)


@dataclass
class Payload:
    name: str
    age: int
