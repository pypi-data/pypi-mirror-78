import logging
import warnings

from typing import Dict

import attr
from nifi.flowfile import FlowFile
from sqs_workers.queue import GenericQueue
from sqs_workers.processors import Processor

from .codec import get_codec, FLOWFILE_CODEC_TYPE

logger = logging.getLogger(__name__)


@attr.s
class NiFiQueue(GenericQueue):
    """This is a rough implementation of JobQueue with some semantics changed for NiFi.

    Usage example.

    from nifi.flowfile import FlowFile
    from nifi.sqs_workers import NiFiQueue
    from sqs_workers import SQSEnv

    sqs = SQSEnv()
    test = sqs.queue("test", NiFiQueue)

    ff = FlowFile(dict(a="1", b="2"), content=b"")
    foo.add_flowfile("test", ff)
    """

    processors = attr.ib(factory=dict)  # type: Dict[str, Processor]

    def processor(self, port_id):
        def fn(processor):
            return self.connect_processor(processor, port_id)

        return fn

    def connect_processor(self, processor, port_id):
        from .processor import NiFiProcessor

        extra = {
            "queue_name": self.name,
            "port_id": port_id,
            "processor": "{}:{}".format(processor.__module__, processor.__name__),
        }
        logger.debug(
            "Connect nifi+sqs://{queue_name}/{port_id} to {processor}".format(**extra),
            extra=extra,
        )
        self.processors[port_id] = NiFiProcessor(self, fn=processor)

    def add_flowfile(
        self,
        port_id: str,
        flowfile: FlowFile,
        response_port_prefix: str = None,
        response_queue_name: str = None,
    ):
        codec = get_codec(FLOWFILE_CODEC_TYPE)
        message_body = codec.serialize([flowfile])

        queue = self.get_queue()
        kwargs = {
            "MessageBody": message_body,
            "MessageAttributes": {
                "ContentType": {
                    "StringValue": FLOWFILE_CODEC_TYPE,
                    "DataType": "String",
                },
                "InputPortId": {"StringValue": port_id, "DataType": "String"},
            },
        }

        response_queue_name = response_queue_name if response_queue_name else self.name
        if response_port_prefix is not None:
            msg_attrs = kwargs["MessageAttributes"]
            msg_attrs["ResponseQueue"] = {
                "StringValue": response_queue_name,
                "DataType": "String",
            }
            msg_attrs["ResponsePortPrefix"] = {
                "StringValue": response_port_prefix,
                "DataType": "String",
            }

        ret = queue.send_message(**kwargs)
        return ret["MessageId"]

    def process_message(self, message):
        input_port_id = self.get_input_port_id(message)
        processor = self.get_processor(input_port_id)
        if processor:
            return processor.process_message(message)
        else:
            warnings.warn(
                "Error processing nifi+sqs://{}/{}".format(self.name, input_port_id)
            )
            return False

    def get_processor(self, port_id):
        return self.processors.get(port_id)

    @staticmethod
    def get_input_port_id(message):
        attrs = message.message_attributes or {}
        return (attrs.get("InputPortId") or {}).get("StringValue")
