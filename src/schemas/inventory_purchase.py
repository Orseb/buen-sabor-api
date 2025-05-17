from datetime import datetime
from typing import Optional

from src.schemas.base import BaseSchema
from src.schemas.inventory_item import ResponseInventoryItemSchema


class BaseInventoryPurchaseSchema(BaseSchema):
    inventory_item_id: int
    quantity: int
    unit_cost: float
    total_cost: float
    notes: Optional[str] = None
    purchase_date: Optional[datetime] = None


class CreateInventoryPurchaseSchema(BaseInventoryPurchaseSchema):
    pass


class ResponseInventoryPurchaseSchema(BaseInventoryPurchaseSchema):
    id_key: int
    purchase_date: datetime
    inventory_item: ResponseInventoryItemSchema
