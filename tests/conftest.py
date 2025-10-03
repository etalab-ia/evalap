import os
import threading
import time

import zmq

os.environ["ENV"] = "unittest"
##We need to do this before importing config

from typing import Generator

import pytest
from fastapi.testclient import TestClient

from evalap.api.config import ZMQ_SENDER_URL
from evalap.api.db import SessionLocal
from evalap.api.main import app

#
# Api client
#


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


#
# DB
#


@pytest.fixture(scope="session")
def db() -> Generator:
    print("Setup session...")
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()
    print("Teardown session.")


#
# MP
#


@pytest.fixture(scope="session", autouse=True)
def zmq_server():
    """Very simple fixture that just listens on a ZMQ port"""

    def listen_thread():
        context = zmq.Context()
        socket = context.socket(zmq.PULL)
        socket.bind(ZMQ_SENDER_URL)  # The port your code is using

        # Keep receiving messages until the test is done
        while not stop_event.is_set():
            try:
                # Non-blocking receive with a timeout
                socket.RCVTIMEO = 100  # 100ms timeout
                socket.recv_json()  # Just receive and discard
            except zmq.error.Again:
                # Timeout occurred, just continue
                pass

        socket.close()
        context.term()

    # Use an event to signal the thread to stop
    stop_event = threading.Event()

    # Start the listener thread
    thread = threading.Thread(target=listen_thread)
    thread.daemon = True
    thread.start()

    # Allow time for the socket to bind
    time.sleep(0.1)

    # Yield nothing, we just need the socket to exist
    yield

    # Signal the thread to stop and wait for it
    stop_event.set()
    thread.join(timeout=1.0)
