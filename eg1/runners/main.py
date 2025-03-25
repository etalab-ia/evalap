import logging
import threading

import zmq

from eg1.api.config import MAX_CONCURRENT_TASKS, ZMQ_SENDER_URL, ZMQ_WORKER_URL
from eg1.clients import MCPBridgeClient
from eg1.logger import logger

from .tasks import process_task

logging.getLogger("httpx").setLevel(logging.WARNING)


def worker_routine(worker_url, context, mcp_bridge):
    """Worker routine"""

    # Socket to pull messages from the dispatcher
    receiver = context.socket(zmq.PULL)
    receiver.connect(worker_url)

    while True:
        try:
            # Receive a task
            message = receiver.recv_json()

            # Process the task
            process_task(message, mcp_bridge)
        except Exception as e:
            logger.exception("An error occurred in the ZMQ main loop: %s", e)


def main(worker_url=ZMQ_WORKER_URL, sender_url=ZMQ_SENDER_URL):
    """server routine"""

    # Prepare our context and sockets
    context = zmq.Context()

    # Socket to pull messages from clients
    receiver = context.socket(zmq.PULL)  # Receives messages
    receiver.bind(sender_url)

    # Socket to push messages to workers
    distributor = context.socket(zmq.PUSH)  # Distributes work
    distributor.bind(worker_url)

    # MCP Bridge client initalization
    try:
        mcp_bridge = MCPBridgeClient()
    except Exception as e:
        logger.warning(
            "MCP bridge is not responding, MCP will not be used."
            f"Reason: {e}"
        )  # fmt: skip
        mcp_bridge = None

    # Launch pool of worker threads
    for i in range(MAX_CONCURRENT_TASKS):
        thread = threading.Thread(target=worker_routine, args=(worker_url, context, mcp_bridge))
        thread.start()

    logger.info(f"ZeroMQ is listening at worker:{worker_url} | receiver:{sender_url}")
    zmq.device(zmq.STREAMER, receiver, distributor)

    # Cleanup
    receiver.close()
    distributor.close()
    context.term()


if __name__ == "__main__":
    main()
