from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from src.models.base import BaseModel
from src.repositories.base import BaseRepository
from src.schemas.base import BaseSchema

T = TypeVar("T", bound=BaseModel)
S = TypeVar("S", bound=BaseSchema)


class BaseService(Generic[T, S], ABC):
    """Abstract base service defining the interface for business logic operations."""

    @property
    @abstractmethod
    def repository(self) -> BaseRepository:
        """Get the repository for data access."""
        pass

    @property
    @abstractmethod
    def schema(self) -> Type[S]:
        """Get the Pydantic schema class for responses."""
        pass

    @property
    @abstractmethod
    def model(self) -> Type[T]:
        """Get the SQLAlchemy model class."""
        pass

    @abstractmethod
    def get_all(self, offset: int = 0, limit: int = 10) -> List[S]:
        """Get all records."""
        pass

    @abstractmethod
    def get_one(self, id_key: int) -> S:
        """Get a record by primary key."""
        pass

    @abstractmethod
    def get_one_by(self, field_name: str, field_value: Any) -> Optional[S]:
        """Get a record by a specific field value."""
        pass

    @abstractmethod
    def save(self, schema: Any) -> S:
        """Save a new record."""
        pass

    @abstractmethod
    def update(self, id_key: int, schema_or_dict: Union[Any, Dict[str, Any]]) -> S:
        """Update an existing record."""
        pass

    @abstractmethod
    def delete(self, id_key: int) -> S:
        """Delete a record by primary key."""
        pass

    @abstractmethod
    def to_model(self, schema: Any) -> T:
        """Convert a schema to a model instance."""
        pass
