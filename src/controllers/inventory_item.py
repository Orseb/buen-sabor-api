from src.controllers.base_implementation import BaseControllerImplementation
from src.schemas.inventory_item import (
    CreateInventoryItemSchema,
    ResponseInventoryItemSchema,
)
from src.services.inventory_item import InventoryItemService


class InventoryItemController(BaseControllerImplementation):
    def __init__(self):
        super().__init__(
            create_schema=CreateInventoryItemSchema,
            response_schema=ResponseInventoryItemSchema,
            service=InventoryItemService(),
            tags=["Inventory Item"],
        )
