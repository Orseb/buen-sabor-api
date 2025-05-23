from typing import List, Optional

from src.schemas.base import BaseSchema


class BaseInventoryItemCategorySchema(BaseSchema):
    name: str
    description: str = None
    active: bool = True
    parent_id: Optional[int] = None


class CreateInventoryItemCategorySchema(BaseInventoryItemCategorySchema):
    pass


class ResponseInventoryItemCategorySchema(CreateInventoryItemCategorySchema):
    id_key: int
    subcategories: List["ResponseInventoryItemCategorySchema"] = []


ResponseInventoryItemCategorySchema.model_rebuild()
