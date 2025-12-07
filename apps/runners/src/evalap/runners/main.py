import logging
import signal
import threading

import zmq

from evalap.core.config import MAX_CONCURRENT_TASKS, ZMQ_SENDER_URL, ZMQ_WORKER_URL
from evalap.clients import MCPBridgeClient
from evalap.logger import logger

from .tasks import process_task

logging.getLogger("httpx").setLevel(logging.WARNING)


def worker_routine(worker_url, context, mcp_bridge, shutdown_event):
    """Worker routine"""

    # Socket to pull messages from the dispatcher
    receiver = context.socket(zmq.PULL)
    receiver.connect(worker_url)

    try:
        while not shutdown_event.is_set():
            try:
                # Receive a task with timeout to allow checking shutdown
                if receiver.poll(1000):  # 1 second timeout
                    message = receiver.recv_json()

                    # Process the task
                    process_task(message, mcp_bridge)
            except zmq.ContextTerminated:
                # Context terminated, exit gracefully
                logger.info("Worker thread: Context terminated, exiting...")
                break
            except zmq.ZMQError as e:
                if e.errno == zmq.ETERM:
                    # Context terminated, exit gracefully
                    logger.info("Worker thread: Context terminated, exiting...")
                    break
                else:
                    logger.exception("ZMQ error in worker thread: %s", e)
            except Exception as e:
                logger.exception("An error occurred in the ZMQ main loop: %s", e)
    finally:
        # Ensure socket is closed
        receiver.close(linger=0)
        logger.info("Worker thread: Socket closed")


def main(worker_url=ZMQ_WORKER_URL, sender_url=ZMQ_SENDER_URL):
    """server routine"""
    # Prepare our context and sockets
    context = zmq.Context()

    # Flag to track shutdown state
    shutdown_event = threading.Event()

    def signal_handler(signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        shutdown_event.set()
        # Don't call sys.exit here, let the main loop handle cleanup

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

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
    worker_threads = []
    for i in range(MAX_CONCURRENT_TASKS):
        thread = threading.Thread(
            target=worker_routine, args=(worker_url, context, mcp_bridge, shutdown_event)
        )
        thread.daemon = True  # Allow threads to exit when main thread exits
        thread.start()
        worker_threads.append(thread)

    logger.info(f"ZeroMQ is listening at worker:{worker_url} | receiver:{sender_url}")

    try:
        # Use a different approach instead of zmq.device to allow graceful shutdown
        poller = zmq.Poller()
        poller.register(receiver, zmq.POLLIN)

        while not shutdown_event.is_set():
            try:
                socks = dict(poller.poll(1000))  # 1 second timeout
                if receiver in socks:
                    message = receiver.recv()
                    distributor.send(message)
            except zmq.ContextTerminated:
                logger.info("ZMQ context terminated, exiting...")
                break
            except zmq.ZMQError as e:
                if e.errno == zmq.ETERM:
                    logger.info("ZMQ context terminated, exiting...")
                    break
                else:
                    raise
            except KeyboardInterrupt:
                logger.info("Received KeyboardInterrupt, shutting down...")
                break

    except Exception as e:
        logger.error(f"Error in main loop: {e}")

    finally:
        # Signal all threads to shutdown
        shutdown_event.set()

        # Cleanup
        logger.info("Cleaning up ZMQ resources...")
        try:
            receiver.close(linger=0)
            distributor.close(linger=0)
            context.term()
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
        logger.info("Runner shutdown complete")


if __name__ == "__main__":
    main()
