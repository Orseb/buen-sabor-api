from src.models.inventory_item_category import InventoryItemCategoryModel
from src.repositories.inventory_item_category import InventoryItemCategoryRepository
from src.schemas.inventory_item_category import (
    CreateInventoryItemCategorySchema,
    ResponseInventoryItemCategorySchema,
)
from src.services.base_implementation import BaseServiceImplementation


class InventoryItemCategoryService(BaseServiceImplementation):

    def __init__(self):
        super().__init__(
            repository=InventoryItemCategoryRepository(),
            model=InventoryItemCategoryModel,
            create_schema=CreateInventoryItemCategorySchema,
            response_schema=ResponseInventoryItemCategorySchema,
        )
