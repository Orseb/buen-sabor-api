from src.controllers.base_implementation import BaseControllerImplementation
from src.schemas.inventory_item_category import (
    CreateInventoryItemCategorySchema,
    ResponseInventoryItemCategorySchema,
)
from src.services.inventory_item_category import InventoryItemCategoryService


class InventoryItemCategoryController(BaseControllerImplementation):
    def __init__(self):
        super().__init__(
            create_schema=CreateInventoryItemCategorySchema,
            response_schema=ResponseInventoryItemCategorySchema,
            service=InventoryItemCategoryService(),
            tags=["Inventory Item Category"],
        )
