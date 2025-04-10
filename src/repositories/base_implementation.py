import logging
from contextlib import contextmanager
from typing import List, Type

from sqlalchemy.orm import Session

from src.config.database import Database
from src.models.base import BaseModel
from src.repositories.base import BaseRepository
from src.schemas.base import BaseSchema


class RecordNotFoundError(Exception):
    """
    RecordNotFoundError is raised when a record is not found
    """


class BaseRepositoryImplementation(BaseRepository):
    """
    Class BaseRepositoryImpl implements BaseRepository
    """

    def __init__(self, model: Type[BaseModel], schema: Type[BaseSchema]):
        self._model = model
        self._schema = schema
        self.logger = logging.getLogger(__name__)
        self._session = Database().get_session()

    @property
    def session(self) -> Session:
        return self._session

    @property
    def model(self) -> Type[BaseModel]:
        return self._model

    @property
    def schema(self) -> Type[BaseSchema]:
        return self._schema

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.session
        try:
            yield session
            session.commit()
        except Exception as e:
            self.logger.error("Session rollback because of error %s", e)
            session.rollback()
            raise
        finally:
            session.close()

    def find(self, id_key: int) -> BaseSchema:
        with self.session_scope() as session:
            model = session.query(self.model).get(id_key)
            if model is None:
                raise RecordNotFoundError(f"No record found with id {id_key}")
            return self.schema.model_validate(model)

    def find_all(self) -> List[BaseSchema]:
        with self.session_scope() as session:
            models = session.query(self.model).all()
            schemas = []
            for model in models:
                schemas.append(self.schema.model_validate(model))
            return schemas

    def save(self, model: BaseModel) -> BaseSchema:
        with self.session_scope() as session:
            session.add(model)
            return self.schema.model_validate(model)

    def update(self, id_key: int, changes: dict) -> BaseSchema:
        with self.session_scope() as session:
            # Filter the instance with the given id_key
            instance = (
                session.query(self.model).filter(self.model.id_key == id_key).first()
            )
            if instance is None:
                raise RecordNotFoundError(f"No record found with id {id_key}")
            # Update the instance with the new data
            for key, value in changes.items():
                if key in instance.__dict__ and value is not None:
                    setattr(instance, key, value)
            session.commit()
            # Retrieve the updated instance
            # Validate the updated instance with the schema
            schema = self.schema.model_validate(instance)
        return schema

    def remove(self, id_key: int) -> None:
        with self.session_scope() as session:
            model = session.query(self.model).get(id_key)
            if model is None:
                raise RecordNotFoundError(f"No record found with id {id_key}")
            session.delete(model)

    def save_all(self, models: List[BaseModel]) -> List[BaseSchema]:
        with self.session_scope() as session:
            session.add_all(models)
            return [self.schema.model_validate(model) for model in models]
