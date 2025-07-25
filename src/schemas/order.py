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
from src.schemas.order_promotion_detail import CreateOrderPromotionDetailSchema
from src.schemas.user import ResponseUserSchema


class BaseOrderSchema(BaseSchema):
    delivery_method: DeliveryMethod
    payment_method: PaymentMethod
    notes: Optional[str] = None


class CreateOrderSchema(BaseOrderSchema):
    user_id: Optional[int] = None
    address_id: Optional[int] = None
    details: List[CreateOrderDetailSchema] = []
    inventory_details: List[CreateOrderInventoryDetailSchema] = []
    promotion_details: List[CreateOrderPromotionDetailSchema] = []


class ResponseOrderSchema(BaseOrderSchema):
    date: Optional[datetime] = None
    payment_id: Optional[str] = None
    estimated_time: Optional[int] = None
    final_total: Optional[float] = None
    discount: Optional[float] = None
    total: Optional[float] = None
    is_paid: bool = False
    status: OrderStatus
    user: ResponseUserSchema
    address: Optional[ResponseAddressSchema] = None
    details: List[ResponseOrderDetailSchema] = []
    inventory_details: List[ResponseOrderInventoryDetailSchema] = []
    invoice_id: Optional[int] = None
    id_key: int
