from typing import Any, Dict, Type, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T", bound="BaseSchema")


class BaseSchema(BaseModel):
    """Base class for all Pydantic schemas in the application."""

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
    )

    @classmethod
    def from_orm(cls: Type[T], obj: Any) -> T:
        """Create a schema instance from an ORM model instance."""
        return cls.model_validate(obj)

    def to_dict(self, exclude_none: bool = True) -> Dict[str, Any]:
        """Convert the schema to a dictionary."""
        return self.model_dump(exclude_none=exclude_none)
