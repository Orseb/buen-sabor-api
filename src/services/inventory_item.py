from src.models.inventory_item import InventoryItemModel
from src.repositories.inventory_item import InventoryItemRepository
from src.schemas.inventory_item import (
    CreateInventoryItemSchema,
    ResponseInventoryItemSchema,
)
from src.services.base_implementation import BaseServiceImplementation


class InventoryItemService(BaseServiceImplementation):

    def __init__(self):
        super().__init__(
            repository=InventoryItemRepository(),
            model=InventoryItemModel,
            create_schema=CreateInventoryItemSchema,
            response_schema=ResponseInventoryItemSchema,
        )
