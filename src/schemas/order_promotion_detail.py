from typing import Optional

from src.schemas.base import BaseSchema


class BaseOrderPromotionDetailSchema(BaseSchema):
    quantity: int


class CreateOrderPromotionDetailSchema(BaseOrderPromotionDetailSchema):
    order_id: Optional[int] = None
    unit_price: Optional[float] = None
    subtotal: Optional[float] = None
    discount_applied: Optional[float] = None
    promotion_id: int
