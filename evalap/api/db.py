from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy_utils import create_database, database_exists

from evalap.api.config import DATABASE_URI, ENV

engine = (
    create_engine(DATABASE_URI, connect_args={"check_same_thread": False}, poolclass=StaticPool)
    if ENV == "unittest"
    else create_engine(DATABASE_URI, pool_size=20, max_overflow=40, pool_recycle=1800, pool_timeout=30)
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def _db_session():
    """Internal context manager for a transactional DB session."""
    db = SessionLocal()
    try:
        with db.begin():
            yield db
    finally:
        db.close()


def get_db():
    """FastAPI dependency for database session with automatic transaction management."""
    with _db_session() as db:
        yield db


@contextmanager
def get_db_context():
    """Context manager for database session with automatic transaction management."""
    with _db_session() as db:
        yield db


def create_database_if_not_exists(database_url: str = DATABASE_URI):
    """Create empty database if it does not exist yet."""
    engine = create_engine(database_url)
    if not database_exists(engine.url):
        create_database(engine.url)
    # Does not work :(
    # conn = engine.connect()
    # conn.execute("commit")
    # conn.execute("CREATE DATABASE IF NOT EXISTS mydatabase")
    # conn.close()
