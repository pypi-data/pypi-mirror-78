import logging
from functools import partial

from nifi.flowfile import FlowFile
from sqs_workers.processors import Processor, get_job_content_type

from .queue import NiFiQueue
from .codec import get_codec

logger = logging.getLogger(__name__)


class NiFiProcessor(Processor):
    """An SQS-Worker Processor that supports different codecs for Context and Content."""

    def process_message(self, message):
        """Accepts different codecs for content_type and context_type."""
        extra = {
            "message_id": message.message_id,
            "queue_name": self.queue.name,
            "port_id": self.job_name,
        }
        logger.debug(
            "Process nifi+sqs://{queue_name}/{port_id}".format(**extra), extra=extra
        )

        try:
            success_callback = self.get_response_callback(message, "success")
            failure_callback = self.get_response_callback(message, "failure")

            content_type = get_job_content_type(message)
            extra["content_type"] = content_type
            codec = get_codec(content_type)

            flowfiles = codec.deserialize(message.body)

            for flowfile in flowfiles:
                self.process_flowfile(flowfile, success_callback, failure_callback)

        except Exception:
            logger.exception(
                "Error while processing nifi+sqs://{queue_name}/{port_id}".format(
                    **extra
                ),
                extra=extra,
            )
            return False
        else:
            return True

    def get_response_callback(self, message, suffix):
        attrs = message.message_attributes
        port_prefix = (attrs.get("ResponsePortPrefix") or {}).get("StringValue")
        if port_prefix is None:
            return lambda *args, **kwargs: None
        port_id = f"{port_prefix}/{suffix}"
        queue = self.get_response_queue(message)
        return partial(queue.add_flowfile, port_id)

    def get_response_queue(self, message):
        attrs = message.message_attributes
        queue_name = (attrs.get("ResponseQueue") or {}).get("StringValue")
        return self.queue.env.queue(queue_name, NiFiQueue)

    def process_flowfile(self, flowfile: FlowFile, success, failure):
        try:
            rvs = self.fn(flowfile)
            for rv in rvs or [flowfile]:
                success(rv)
        except Exception:
            failure(flowfile)
