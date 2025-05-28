import logging
from contextlib import contextmanager
from typing import Any, Dict, Generic, Iterator, List, Optional, Type, TypeVar

from sqlalchemy.orm import Session, scoped_session, sessionmaker

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
        self._session_factory = scoped_session(sessionmaker(bind=Database().engine))

    @property
    def session(self):
        raise NotImplementedError(
            "Direct session access is not supported. Use session_scope()."
        )

    @property
    def model(self) -> Type[T]:
        """Get the SQLAlchemy model class."""
        return self._model

    @property
    def schema(self) -> Type[S]:
        """Get the Pydantic schema class for responses."""
        return self._response_schema

    @contextmanager
    def session_scope(self) -> Iterator[Session]:
        """Provide a transactional scope around a series of operations."""
        session: Session = self._session_factory()
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
        """Find record with id_key."""
        with self.session_scope() as session:
            model = session.get(self.model, id_key)
            if model is None or not getattr(model, "active", True):
                raise RecordNotFoundError(f"No record found with id {id_key}")
            return self.schema.model_validate(model)

    def find_by(self, field_name: str, field_value: Any) -> Optional[S]:
        """Find a record by a specific field value."""
        with self.session_scope() as session:
            model = (
                session.query(self.model)
                .filter(getattr(self.model, field_name) == field_value)
                .filter_by(active=True)
                .first()
            )
            if model is None:
                return None
            return self.schema.model_validate(model)

    def find_all_by(
        self, field_name: str, field_value: Any, offset: int, limit: int
    ) -> List[S]:
        """Find all records by a specific field value."""
        with self.session_scope() as session:
            models = (
                session.query(self.model)
                .filter(getattr(self.model, field_name) == field_value)
                .filter_by(active=True)
                .offset(offset)
                .limit(limit)
                .all()
            )
            return [self.schema.model_validate(model) for model in models]

    def find_all(self, offset: int = 0, limit: int = 10) -> List[S]:
        """Find all records."""
        with self.session_scope() as session:
            models = (
                session.query(self.model)
                .filter_by(active=True)
                .offset(offset)
                .limit(limit)
                .all()
            )
            return [self.schema.model_validate(model) for model in models]

    def save(self, model: T) -> S:
        """Save a new record."""
        with self.session_scope() as session:
            session.add(model)
            session.flush()
            session.refresh(model)
            return self.schema.model_validate(model)

    def update(self, id_key: int, changes: Dict[str, Any]) -> S:
        """Update an existing record."""
        with self.session_scope() as session:
            model = session.get(self.model, id_key)
            if model is None:
                raise RecordNotFoundError(f"No record found with id {id_key}")

            for key, value in changes.items():
                if hasattr(model, key) and value is not None:
                    setattr(model, key, value)

            session.flush()
            session.refresh(model)
            return self.schema.model_validate(model)

    def remove(self, id_key: int) -> S:
        """Soft delete a record by primary key."""
        with self.session_scope() as session:
            model = session.get(self.model, id_key)
            if model is None:
                raise RecordNotFoundError(f"No record found with id {id_key}")
            model.active = False
            session.add(model)
            session.flush()
            session.refresh(model)
            return self.schema.model_validate(model)
