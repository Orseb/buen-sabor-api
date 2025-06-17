from typing import List, Optional

from src.schemas.base import BaseSchema


class BaseInventoryItemCategorySchema(BaseSchema):
    name: str
    description: str = None
    active: bool = True
    public: Optional[bool] = False


class CreateInventoryItemCategorySchema(BaseInventoryItemCategorySchema):
    parent_id: Optional[int] = None


class ResponseInventoryItemCategorySchema(CreateInventoryItemCategorySchema):
    id_key: int
    subcategories: List["ResponseInventoryItemCategorySchema"] = []


class ResponseParentPublicInventoryItemCategorySchema(BaseInventoryItemCategorySchema):
    id_key: int


class ResponsePublicInventoryItemCategorySchema(BaseInventoryItemCategorySchema):
    id_key: int
    parent: Optional["ResponseParentPublicInventoryItemCategorySchema"] = None
