from datetime import datetime
from typing import List, Optional

from src.models.order import DeliveryMethod, OrderStatus, PaymentMethod
from src.schemas.address import ResponseAddressSchema
from src.schemas.base import BaseSchema
from src.schemas.order_detail import CreateOrderDetailSchema, ResponseOrderDetailSchema
from src.schemas.order_inventory_detail import (
    CreateOrderInventoryDetailSchema,
    ResponseOrderInventoryDetailSchema,
)
from src.schemas.user import ResponseUserSchema


class BaseOrderSchema(BaseSchema):
    date: Optional[datetime] = None
    total: float
    discount: float = 0.0
    final_total: float
    status: OrderStatus = OrderStatus.a_confirmar
    estimated_time: Optional[int] = None
    delivery_method: DeliveryMethod
    payment_method: PaymentMethod
    payment_id: Optional[str] = None
    is_paid: bool = False
    notes: Optional[str] = None


class CreateOrderSchema(BaseOrderSchema):
    user_id: Optional[int] = None
    address_id: Optional[int] = None
    details: List[CreateOrderDetailSchema] = []
    inventory_details: List[CreateOrderInventoryDetailSchema] = []


class ResponseOrderSchema(BaseOrderSchema):
    user: ResponseUserSchema
    address: Optional[ResponseAddressSchema] = None
    details: List[ResponseOrderDetailSchema] = []
    inventory_details: List[ResponseOrderInventoryDetailSchema] = []
    id_key: int
