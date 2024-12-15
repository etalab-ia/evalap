import logging
import threading

import zmq

from api.config import MAX_CONCURRENT_TASKS

from .tasks import process_task

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)


def worker_routine(worker_url, context):
    """Worker routine"""

    # Socket to pull messages from the dispatcher
    socket = context.socket(zmq.PULL)
    socket.connect(worker_url)

    while True:
        try:
            # Receive a task
            message = socket.recv_json()

            # Process the task
            process_task(message)
        except Exception as e:
            logger.exception("An error occurred in the ZMQ main loop: %s", e)


def main():
    """server routine"""

    url_worker = "inproc://workers"
    url_client = "tcp://localhost:5555"

    # Prepare our context and sockets
    context = zmq.Context()

    # Socket to pull messages from clients
    clients = context.socket(zmq.PULL)
    clients.bind(url_client)

    # Socket to talk to workers
    workers = context.socket(zmq.PUSH)
    workers.bind(url_worker)

    # Launch pool of worker threads
    for i in range(MAX_CONCURRENT_TASKS):
        thread = threading.Thread(target=worker_routine, args=(url_worker, context))
        thread.start()

    logger.info(f"ZeroMQ is listening at {url_worker} | {url_client}")
    zmq.device(zmq.STREAMER, clients, workers)

    # Cleanup
    clients.close()
    workers.close()
    context.term()


if __name__ == "__main__":
    main()
