from evalap.api.db import engine
from evalap.api.models import Base


class TestApi:
    """Base test class that all test classes should inherit from."""

    def setup_method(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        # eventually initialize db data.
        # db: Session = SessionLocal()
