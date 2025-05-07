from datetime import datetime
from typing import List, Optional

from pydantic import validator

from src.models.order import DeliveryMethod, OrderStatus, PaymentMethod
from src.schemas.address import ResponseAddressSchema
from src.schemas.base import BaseSchema
from src.schemas.order_detail import CreateOrderDetailSchema, ResponseOrderDetailSchema
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

    @validator("payment_method")
    def validate_payment_method(cls, v, values):
        if (
            "delivery_method" in values
            and values["delivery_method"] == DeliveryMethod.delivery
        ):
            if v != PaymentMethod.mercado_pago:
                raise ValueError(
                    "Delivery orders must use Mercado Pago as payment method"
                )
        return v


class CreateOrderSchema(BaseOrderSchema):
    user_id: int
    address_id: Optional[int] = None
    details: List[CreateOrderDetailSchema] = []

    @validator("address_id")
    def validate_address(cls, v, values):
        if (
            "delivery_method" in values
            and values["delivery_method"] == DeliveryMethod.delivery
        ):
            if v is None:
                raise ValueError("Delivery orders must have an address")
        return v


class ResponseOrderSchema(BaseOrderSchema):
    user: ResponseUserSchema
    address: Optional[ResponseAddressSchema] = None
    details: List[ResponseOrderDetailSchema] = []
    id_key: int
