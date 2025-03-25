from sqlalchemy.orm import Session

from eg1.api.db import engine, SessionLocal
from eg1.api.models import Base


class TestApi:
    """Base test class that all test classes should inherit from."""

    def setup_method(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        # eventually initialize db data.
        #db: Session = SessionLocal()

