from typing import Optional

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from .settings import settings

DATABASE_URL = (
    f"postgresql://{settings.db_username}"
    f":{settings.db_password}"
    f"@{settings.db_host}"
    f":{settings.db_port}"
    f"/{settings.db_name}"
)


class Database:
    """Clase para manejar la conexión a la base de datos PostgreSQL"""

    _instance: Optional["Database"] = None
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def __new__(cls) -> "Database":
        """Implementación del patrón Singleton"""
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._engine = cls.engine
            cls._instance._SessionLocal = cls.SessionLocal
            cls._instance._session = None
        return cls._instance

    def check_connection(self) -> str:
        """Verifica la conexión a la base de datos ejecutando una consulta simple"""
        try:
            with self._engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return "Connection successful"
        except Exception as e:
            return f"Connection failed: {e}"
