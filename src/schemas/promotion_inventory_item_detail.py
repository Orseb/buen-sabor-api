from src.schemas.base import BaseSchema
from src.schemas.inventory_item import ResponseInventoryItemSchema


class BasePromotionInventoryItemDetailSchema(BaseSchema):
    quantity: int


class CreatePromotionInventoryItemDetailSchema(BasePromotionInventoryItemDetailSchema):
    inventory_item_id: int


class ResponsePromotionInventoryItemDetailSchema(
    BasePromotionInventoryItemDetailSchema
):
    id_key: int
    inventory_item: ResponseInventoryItemSchema
