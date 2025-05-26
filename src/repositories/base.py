"""
Base repository interface defining standard data access methods.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from sqlalchemy.orm import Session

from src.models.base import BaseModel
from src.schemas.base import BaseSchema

T = TypeVar("T", bound=BaseModel)
S = TypeVar("S", bound=BaseSchema)


class BaseRepository(Generic[T, S], ABC):
    """Abstract base repository defining the interface for data access operations."""

    @property
    @abstractmethod
    def session(self) -> Session:
        """Get the SQLAlchemy session."""
        pass

    @property
    @abstractmethod
    def model(self) -> Type[T]:
        """Get the SQLAlchemy model class."""
        pass

    @property
    @abstractmethod
    def schema(self) -> Type[S]:
        """Get the Pydantic schema class for responses."""
        pass

    @abstractmethod
    def find(self, offset: int = 0, limit: int = 10) -> List[S]:
        """Find records."""
        pass

    @abstractmethod
    def find_by(self, field_name: str, field_value: Any) -> Optional[S]:
        """Find a record by a specific field value."""
        pass

    @abstractmethod
    def find_all(self) -> List[S]:
        """Find all records."""
        pass

    @abstractmethod
    def save(self, model: T) -> S:
        """Save a new record."""
        pass

    @abstractmethod
    def update(self, id_key: int, changes: Dict[str, Any]) -> S:
        """Update an existing record."""
        pass

    @abstractmethod
    def remove(self, id_key: int) -> S:
        """Delete a record by primary key."""
        pass

    @abstractmethod
    def save_all(self, models: List[T]) -> List[S]:
        """Save multiple records."""
        pass
