from typing import List, Optional

from src.schemas.base import BaseSchema
from src.schemas.promotion_inventory_item_detail import (
    CreatePromotionInventoryItemDetailSchema,
    ResponsePromotionInventoryItemDetailSchema,
)
from src.schemas.promotion_manufactured_item_detail import (
    CreatePromotionManufacturedItemDetailSchema,
    ResponsePromotionManufacturedItemDetailSchema,
)


class BasePromotionSchema(BaseSchema):
    name: str
    description: Optional[str] = None
    discount_percentage: float
    active: bool = True


class CreatePromotionSchema(BasePromotionSchema):
    manufactured_item_details: List[CreatePromotionManufacturedItemDetailSchema] = []
    inventory_item_details: List[CreatePromotionInventoryItemDetailSchema] = []


class ResponsePromotionSchema(BasePromotionSchema):
    id_key: int
    manufactured_item_details: List[ResponsePromotionManufacturedItemDetailSchema] = []
    inventory_item_details: List[ResponsePromotionInventoryItemDetailSchema] = []
