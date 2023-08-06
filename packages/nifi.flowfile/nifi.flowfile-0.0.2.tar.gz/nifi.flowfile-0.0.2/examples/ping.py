import uuid

from sqs_workers import SQSEnv, create_standard_queue, delete_queue

from nifi.flowfile import FlowFile
from nifi.sqs_workers import NiFiQueue

# This environment will use AWS
from sqs_workers.shutdown_policies import MaxTasksShutdown

sqs = SQSEnv()

# Create a new queue.
queue_name = str(uuid.uuid4())
create_standard_queue(sqs, queue_name)

# Get the queue object
queue = sqs.queue(queue_name, NiFiQueue)


@queue.processor("ping")
def ping(flowfile: FlowFile):
    print("Ping...")


@queue.processor("ping/success")
def pong(flowfile: FlowFile):
    print("Pong...")


# Start PingPong
ff = FlowFile({"a": "1"})

try:
    queue.add_flowfile(
        "ping", ff, response_queue_name=queue_name, response_port_prefix="ping"
    )
    queue.process_queue(shutdown_policy=MaxTasksShutdown(2))
finally:
    delete_queue(sqs, queue_name)
