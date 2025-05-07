from typing import Optional

from src.schemas.base import BaseSchema
from src.schemas.inventory_item import ResponseInventoryItemSchema


class BaseManufacturedItemDetailSchema(BaseSchema):
    quantity: float


class CreateManufacturedItemDetailSchema(BaseManufacturedItemDetailSchema):
    manufactured_item_id: Optional[int] = None
    inventory_item_id: int


class ResponseManufacturedItemDetailSchema(BaseManufacturedItemDetailSchema):
    manufactured_item_id: int
    inventory_item: ResponseInventoryItemSchema
    id_key: int
