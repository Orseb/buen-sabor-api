from typing import List, Optional

from src.schemas.base import BaseSchema


class BaseManufacturedItemCategorySchema(BaseSchema):
    name: str
    description: str = None
    active: bool = True


class CreateManufacturedItemCategorySchema(BaseManufacturedItemCategorySchema):
    parent_id: Optional[int] = None


class ResponseManufacturedItemCategorySchema(CreateManufacturedItemCategorySchema):
    id_key: int
    subcategories: List["ResponseManufacturedItemCategorySchema"] = []


class ResponseParentPublicManufacturedItemCategorySchema(
    BaseManufacturedItemCategorySchema
):
    id_key: int


class ResponsePublicManufacturedItemCategorySchema(BaseManufacturedItemCategorySchema):
    id_key: int
    parent: Optional["ResponseParentPublicManufacturedItemCategorySchema"] = None
