from typing import Optional

from src.schemas.base import BaseSchema
from src.schemas.inventory_item_category import ResponseInventoryItemCategorySchema
from src.schemas.measurement_unit import ResponseMeasurementUnitSchema


class BaseInventoryItemSchema(BaseSchema):
    name: str
    current_stock: float
    minimum_stock: float
    price: float
    purchase_cost: float
    image_url: Optional[str] = None
    active: bool = True
    is_ingredient: bool = True


class CreateInventoryItemSchema(BaseInventoryItemSchema):
    measurement_unit_id: Optional[int] = None
    category_id: int


class ResponseInventoryItemSchema(BaseInventoryItemSchema):
    measurement_unit: Optional[ResponseMeasurementUnitSchema] = None
    category: ResponseInventoryItemCategorySchema
    id_key: int


class UpdateStockInventoryItemSchema(BaseSchema):
    current_stock: float
