import asyncio
import logging
from concurrent.futures import ProcessPoolExecutor

import zmq
import zmq.asyncio

from api.config import MAX_CONCURRENT_TASKS

from .tasks import process_task

ZMQ_URL = "tcp://localhost:5555"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)


async def run_blocking_task_in_executor(task, semaphore):
    # The aproach with the ProcessPoolExecutor is more efficient got CPU bound task, but have a higher overload.
    # asyncio.to_thread is good for bypassing the GIL and I/O bound task.
    # --
    # loop = asyncio.get_running_loop()
    # with ProcessPoolExecutor() as executor:
    #     await loop.run_in_executor(executor, process_task, task)

    # Acquire a semaphore before processing the task
    async with semaphore:
        return await asyncio.to_thread(process_task, task)


async def worker(url, semaphore):
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.PULL)
    socket.connect(url)  # Connect to the producer's socket
    logger.info(f"ZeroMQ is listening at {url}")

    while True:
        try:
            # Receive a task
            message = await socket.recv_json()

            # Process the task
            asyncio.create_task(run_blocking_task_in_executor(message, semaphore))
        except Exception as e:
            logger.exception("An error occurred in the ZMQ main loop: %s", e)


async def main():
    # Create a semaphore to limit concurrency
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)

    # Start the worker
    await worker(ZMQ_URL, semaphore)


if __name__ == "__main__":
    asyncio.run(main())
