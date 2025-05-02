from src.models.inventory_item_category import InventoryItemCategoryModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.inventory_item_category import (
    CreateInventoryItemCategorySchema,
    ResponseInventoryItemCategorySchema,
)


class InventoryItemCategoryRepository(BaseRepositoryImplementation):
    def __init__(self):
        super().__init__(
            model=InventoryItemCategoryModel,
            create_schema=CreateInventoryItemCategorySchema,
            response_schema=ResponseInventoryItemCategorySchema,
        )
