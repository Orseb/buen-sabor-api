from typing import Optional

from src.schemas.base import BaseSchema
from src.schemas.manufactured_item import ResponseManufacturedItemSchema


class BaseOrderDetailSchema(BaseSchema):
    quantity: int


class CreateOrderDetailSchema(BaseOrderDetailSchema):
    order_id: Optional[int] = None
    unit_price: Optional[float] = None
    subtotal: Optional[float] = None
    manufactured_item_id: int


class ResponseOrderDetailSchema(BaseOrderDetailSchema):
    unit_price: float
    subtotal: float
    order_id: int
    manufactured_item: ResponseManufacturedItemSchema
    id_key: int
