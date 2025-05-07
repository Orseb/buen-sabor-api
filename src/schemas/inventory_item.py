from src.schemas.base import BaseSchema
from src.schemas.inventory_item_category import ResponseInventoryItemCategorySchema
from src.schemas.measurement_unit import ResponseMeasurementUnitSchema


class BaseInventoryItemSchema(BaseSchema):
    name: str
    current_stock: int
    minimum_stock: int
    price: float
    purchase_cost: float
    active: bool = True
    is_ingredient: bool = True


class CreateInventoryItemSchema(BaseInventoryItemSchema):
    measurement_unit_id: int
    category_id: int


class ResponseInventoryItemSchema(BaseInventoryItemSchema):
    measurement_unit: ResponseMeasurementUnitSchema
    category: ResponseInventoryItemCategorySchema
    id_key: int


class UpdateStockInventoryItemSchema(BaseSchema):
    current_stock: int
