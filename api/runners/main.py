import asyncio
import logging

import zmq
import zmq.asyncio

from .tasks import process_task

ZMQ_URL = "tcp://localhost:5555"
MAX_CONCURRENT_TASKS = 32

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def worker(url, semaphore):
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.PULL)
    socket.connect(url)  # Connect to the producer's socket
    logger.info(f"ZeroMQ is listening at {url}")

    while True:
        try:
            # Receive a task
            message = await socket.recv_json()

            # Acquire a semaphore before processing the task
            async with semaphore:
                # Process the task
                await process_task(message)
        except Exception as e:
            logger.exception("An error occurred in the ZMQ main loop: %s", e)


async def main():
    # Create a semaphore to limit concurrency
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)

    # Start the worker
    await worker(ZMQ_URL, semaphore)


if __name__ == "__main__":
    asyncio.run(main())
