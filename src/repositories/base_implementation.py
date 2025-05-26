import logging
from contextlib import contextmanager
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, cast

from sqlalchemy.orm import Session

from src.config.database import Database
from src.models.base import BaseModel
from src.repositories.base import BaseRepository
from src.schemas.base import BaseSchema

T = TypeVar("T", bound=BaseModel)
S = TypeVar("S", bound=BaseSchema)


class RecordNotFoundError(Exception):
    """Exception raised when a record is not found in the database."""

    pass


class BaseRepositoryImplementation(Generic[T, S], BaseRepository[T, S]):
    """Generic implementation of the BaseRepository interface."""

    def __init__(
        self,
        model: Type[T],
        create_schema: Type[BaseSchema],
        response_schema: Type[S],
    ):
        """Initialize the repository with model and schema types."""
        self._model = model
        self._create_schema = create_schema
        self._response_schema = response_schema
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self._session = Database().get_session()

    @property
    def session(self) -> Session:
        """Get the SQLAlchemy session."""
        return self._session

    @property
    def model(self) -> Type[T]:
        """Get the SQLAlchemy model class."""
        return self._model

    @property
    def schema(self) -> Type[S]:
        """Get the Pydantic schema class for responses."""
        return self._response_schema

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.session
        try:
            yield session
            session.commit()
        except Exception as e:
            self.logger.error("Session rollback because of error: %s", str(e))
            session.rollback()
            raise
        finally:
            session.close()

    def find(self, id_key: int) -> S:
        """Find a record by primary key."""
        with self.session_scope() as session:
            model = session.query(self.model).get(id_key)
            if model is None:
                raise RecordNotFoundError(f"No record found with id {id_key}")
            return cast(S, self.schema.model_validate(model))

    def find_by(self, field_name: str, field_value: Any) -> Optional[S]:
        """Find a record by a specific field value."""
        with self.session_scope() as session:
            model = (
                session.query(self.model)
                .filter(getattr(self.model, field_name) == field_value)
                .first()
            )
            if model is None:
                return None
            return cast(S, self.schema.model_validate(model))

    def find_all(self) -> List[S]:
        """Find all records."""
        with self.session_scope() as session:
            models = session.query(self.model).all()
            return [cast(S, self.schema.model_validate(model)) for model in models]

    def save(self, model: T) -> S:
        """Save a new record."""
        with self.session_scope() as session:
            session.add(model)
            session.flush()
            session.refresh(model)
            return cast(S, self.schema.model_validate(model))

    def update(self, id_key: int, changes: Dict[str, Any]) -> S:
        """Update an existing record."""
        with self.session_scope() as session:
            instance = (
                session.query(self.model).filter(self.model.id_key == id_key).first()
            )
            if instance is None:
                raise RecordNotFoundError(f"No record found with id {id_key}")

            for key, value in changes.items():
                if hasattr(instance, key) and value is not None:
                    setattr(instance, key, value)

            session.flush()
            session.refresh(instance)
            return cast(S, self.schema.model_validate(instance))

    def remove(self, id_key: int) -> S:
        """Delete a record by primary key."""
        with self.session_scope() as session:
            model = session.query(self.model).get(id_key)
            if model is None:
                raise RecordNotFoundError(f"No record found with id {id_key}")
            schema = cast(S, self.schema.model_validate(model))
            session.delete(model)
            return schema

    def save_all(self, models: List[T]) -> List[S]:
        """Save multiple records."""
        with self.session_scope() as session:
            session.add_all(models)
            session.flush()
            return [cast(S, self.schema.model_validate(model)) for model in models]
