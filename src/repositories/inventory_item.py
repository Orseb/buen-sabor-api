from src.models.inventory_item import InventoryItemModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.inventory_item import (
    CreateInventoryItemSchema,
    ResponseInventoryItemSchema,
)


class InventoryItemRepository(BaseRepositoryImplementation):
    def __init__(self):
        super().__init__(
            model=InventoryItemModel,
            create_schema=CreateInventoryItemSchema,
            response_schema=ResponseInventoryItemSchema,
        )
