from abc import ABC, abstractmethod
from typing import Generic, List, Type, TypeVar

from src.schemas.base import BaseSchema
from src.services.base import BaseService

S = TypeVar("S", bound=BaseSchema)


class BaseController(Generic[S], ABC):
    """Abstract base controller defining the interface for HTTP endpoints."""

    @property
    @abstractmethod
    def service(self) -> BaseService:
        """Get the service for business logic."""
        pass

    @property
    @abstractmethod
    def schema(self) -> Type[S]:
        """Get the Pydantic schema class for responses."""
        pass

    @abstractmethod
    def get_all(self) -> List[S]:
        """Get all records."""
        pass

    @abstractmethod
    def get_one(self, id_key: int) -> S:
        """Get a record by primary key."""
        pass

    @abstractmethod
    def save(self, schema: BaseSchema) -> S:
        """Save a new record."""
        pass

    @abstractmethod
    def update(self, id_key: int, schema: BaseSchema) -> S:
        """Update an existing record."""
        pass

    @abstractmethod
    def delete(self, id_key: int) -> S:
        """Delete a record by primary key."""
        pass
