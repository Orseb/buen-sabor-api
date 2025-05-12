from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, cast

from src.models.base import BaseModel
from src.repositories.base import BaseRepository
from src.schemas.base import BaseSchema
from src.services.base import BaseService

T = TypeVar("T", bound=BaseModel)
S = TypeVar("S", bound=BaseSchema)


class BaseServiceImplementation(Generic[T, S], BaseService[T, S]):
    """Generic implementation of the BaseService interface."""

    def __init__(
        self,
        repository: BaseRepository,
        model: Type[T],
        create_schema: Type[BaseSchema],
        response_schema: Type[S],
    ):
        """Initialize the service with repository, model, and schema types."""
        self._repository = repository
        self._model = model
        self.create_schema = create_schema
        self.response_schema = response_schema

    @property
    def repository(self) -> BaseRepository:
        """Get the repository for data access."""
        return self._repository

    @property
    def schema(self) -> Type[S]:
        """Get the Pydantic schema class for responses."""
        return self.response_schema

    @property
    def model(self) -> Type[T]:
        """Get the SQLAlchemy model class."""
        return self._model

    def get_all(self) -> List[S]:
        """Get all records."""
        return self.repository.find_all()

    def get_one(self, id_key: int) -> S:
        """Get a record by primary key."""
        return self.repository.find(id_key)

    def get_one_by(self, field_name: str, field_value: Any) -> Optional[S]:
        """Get a record by a specific field value."""
        return self.repository.find_by(field_name, field_value)

    def save(self, schema: Any) -> S:
        """Save a new record."""
        model_instance = self.to_model(schema)
        return self.repository.save(model_instance)

    def update(self, id_key: int, schema_or_dict: Union[Any, Dict[str, Any]]) -> S:
        """Update an existing record."""

        if isinstance(schema_or_dict, dict):
            changes = schema_or_dict
        else:
            changes = schema_or_dict.model_dump(exclude_unset=True)

        return self.repository.update(id_key, changes)

    def delete(self, id_key: int) -> S:
        """Delete a record by primary key."""
        return self.repository.remove(id_key)

    def to_model(self, schema: Any) -> T:
        """Convert a schema to a model instance."""
        model_class = self.model
        model_data = schema.model_dump(exclude_unset=True)
        model_instance = model_class(**model_data)
        return cast(T, model_instance)

    @repository.setter
    def repository(self, value: BaseRepository) -> None:
        self._repository = value

    @model.setter
    def model(self, value: Type[T]) -> None:
        self._model = value

    @schema.setter
    def schema(self, value: Type[S]) -> None:
        self.response_schema = value
