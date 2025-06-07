from typing import Optional

from src.schemas.base import BaseSchema
from src.schemas.inventory_item import ResponseInventoryItemSchema


class BaseOrderInventoryDetailSchema(BaseSchema):
    quantity: int


class CreateOrderInventoryDetailSchema(BaseOrderInventoryDetailSchema):
    order_id: Optional[int] = None
    unit_price: Optional[float] = None
    subtotal: Optional[float] = None
    inventory_item_id: int


class ResponseOrderInventoryDetailSchema(CreateOrderInventoryDetailSchema):
    unit_price: float
    subtotal: float
    order_id: int
    inventory_item: ResponseInventoryItemSchema
    id_key: int
