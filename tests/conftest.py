import os

os.environ["ENV"] = "unittest"
##We need to do this before importing config

from typing import Generator

import pytest
from fastapi.testclient import TestClient

from eg1.api.main import app

from eg1.api.db import SessionLocal


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
