from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from .settings import settings

db_user = settings.db_username
db_pass = settings.db_password
db_host = settings.db_host
db_port = settings.db_port
db_name = settings.db_name

DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"


class Database:
    _instance = None
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def __init__(self):
        self._session = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._engine = cls.engine
            cls._instance._SessionLocal = cls.SessionLocal
        return cls._instance

    def get_session(self) -> Session:
        if self._session is None:
            self._session = self._SessionLocal()
        return self._session

    def check_connection(self):
        try:
            with self._engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            print("Connection established.")
            return True
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return False
