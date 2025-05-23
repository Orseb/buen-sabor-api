from typing import List, Optional

from src.schemas.base import BaseSchema


class BaseManufacturedItemCategorySchema(BaseSchema):
    name: str
    description: str = None
    active: bool = True
    parent_id: Optional[int] = None


class CreateManufacturedItemCategorySchema(BaseManufacturedItemCategorySchema):
    pass


class ResponseManufacturedItemCategorySchema(CreateManufacturedItemCategorySchema):
    id_key: int
    subcategories: List["ResponseManufacturedItemCategorySchema"] = []


ResponseManufacturedItemCategorySchema.model_rebuild()
