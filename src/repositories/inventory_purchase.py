from src.models.inventory_purchase import InventoryPurchaseModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.inventory_purchase import (
    CreateInventoryPurchaseSchema,
    ResponseInventoryPurchaseSchema,
)


class InventoryPurchaseRepository(BaseRepositoryImplementation):
    def __init__(self):
        super().__init__(
            model=InventoryPurchaseModel,
            create_schema=CreateInventoryPurchaseSchema,
            response_schema=ResponseInventoryPurchaseSchema,
        )
