from contextlib import contextmanager
from typing import Optional

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from .settings import settings

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
    engine = create_engine(DATABASE_URL)
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
            self._session = self._SessionLocal()
        return self._session

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self._SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def check_connection(self) -> bool:
        """Check if database connection is working."""
        try:
            with self._engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return True
        except Exception:
            return False
