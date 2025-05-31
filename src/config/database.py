import logging
from contextlib import contextmanager
from typing import Optional

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from .settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = (
    f"postgresql://{settings.db_username}"
    f":{settings.db_password}"
    f"@{settings.db_host}"
    f":{settings.db_port}"
    f"/{settings.db_name}"
)


class Database:
    """Database connection manager with singleton pattern."""

    _instance: Optional["Database"] = None
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def __new__(cls) -> "Database":
        """Ensure only one instance of Database exists."""
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._engine = cls.engine
            cls._instance._SessionLocal = cls.SessionLocal
            cls._instance._session = None
        return cls._instance

    def get_session(self) -> Session:
        """Get a database session."""
        if self._session is None:
            try:
                self._session = self._SessionLocal()
            except Exception as e:
                logger.error(f"Failed to create a session: {e}")
                raise
        return self._session

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self._SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Transaction failed: {e}")
            raise
        finally:
            session.close()

    def check_connection(self) -> str:
        """Check if database connection is working."""
        try:
            with self._engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return "Connection successful"
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return f"Connection failed: {e}"
