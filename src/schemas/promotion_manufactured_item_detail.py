from src.schemas.base import BaseSchema
from src.schemas.manufactured_item import ResponseManufacturedItemSchema


class BasePromotionManufacturedItemDetailSchema(BaseSchema):
    quantity: int


class CreatePromotionManufacturedItemDetailSchema(
    BasePromotionManufacturedItemDetailSchema
):
    manufactured_item_id: int


class ResponsePromotionManufacturedItemDetailSchema(
    BasePromotionManufacturedItemDetailSchema
):
    id_key: int
    manufactured_item: ResponseManufacturedItemSchema
