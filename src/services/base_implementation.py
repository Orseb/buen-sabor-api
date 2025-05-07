from typing import Any, Dict, List, Type, Union

from src.models.base import BaseModel
from src.repositories.base import BaseRepository
from src.schemas.base import BaseSchema
from src.services.base import BaseService


class BaseServiceImplementation(BaseService):
    """Base Service Implementation"""

    def __init__(
        self,
        repository: BaseRepository,
        model: Type[BaseModel],
        create_schema: Type[BaseSchema],
        response_schema: Type[BaseSchema],
    ):
        self.repository = repository
        self.model = model
        self.create_schema = create_schema
        self.response_schema = response_schema

    @property
    def repository(self) -> BaseRepository:
        """Repository to access database"""
        return self._repository

    @property
    def schema(self) -> Type[BaseSchema]:
        """Pydantic Schema to validate data"""
        return self.response_schema

    @property
    def model(self) -> BaseModel:
        """SQLAlchemy Model"""
        return self._model

    def get_all(self) -> List[BaseSchema]:
        """Get all data"""
        return self.repository.find_all()

    def get_one(self, id_key: int) -> BaseSchema:
        """Get one data"""
        return self.repository.find(id_key)

    def get_one_by(self, field_name: str, field_value: any):
        """Get one data by field"""
        return self.repository.find_by(field_name, field_value)

    def save(self, schema: BaseSchema) -> BaseSchema:
        """Save data"""
        return self.repository.save(self.to_model(schema))

    def update(
        self, id_key: int, schema_or_dict: Union[BaseSchema, Dict[str, Any]]
    ) -> BaseSchema:
        """Update data"""
        # Check if schema_or_dict is a dictionary or a Pydantic schema
        if isinstance(schema_or_dict, dict):
            changes = schema_or_dict
        else:
            changes = schema_or_dict.model_dump()

        return self.repository.update(id_key, changes)

    def delete(self, id_key: int) -> BaseSchema:
        """Delete data"""
        return self.repository.remove(id_key)

    def to_model(self, schema: BaseSchema) -> BaseModel:
        model_class = type(self.model) if not callable(self.model) else self.model
        model_instance = model_class(**schema.model_dump())
        return model_instance

    @repository.setter
    def repository(self, value):
        self._repository = value

    @model.setter
    def model(self, value):
        self._model = value

    @schema.setter
    def schema(self, value):
        self.response_schema = value
