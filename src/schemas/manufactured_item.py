from typing import List, Optional

from src.schemas.base import BaseSchema
from src.schemas.manufactured_item_category import (
    ResponseManufacturedItemCategorySchema,
)
from src.schemas.manufactured_item_detail import (
    CreateManufacturedItemDetailSchema,
    ResponseManufacturedItemDetailSchema,
)


class BaseManufacturedItemSchema(BaseSchema):
    name: str
    description: Optional[str] = None
    preparation_time: int
    price: float
    image_url: Optional[str] = None
    recipe: Optional[str] = None
    active: bool = True


class CreateManufacturedItemSchema(BaseManufacturedItemSchema):
    category_id: int
    details: List[CreateManufacturedItemDetailSchema] = []


class ResponseManufacturedItemSchema(BaseManufacturedItemSchema):
    category: ResponseManufacturedItemCategorySchema
    details: List[ResponseManufacturedItemDetailSchema] = []
    id_key: int


class ResponseManufacturedItemWithAvailabilitySchema(ResponseManufacturedItemSchema):
    is_available: bool
