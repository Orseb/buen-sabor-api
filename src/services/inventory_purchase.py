from datetime import datetime
from typing import Optional

from src.models.inventory_purchase import InventoryPurchaseModel
from src.repositories.inventory_item import InventoryItemRepository
from src.repositories.inventory_purchase import InventoryPurchaseRepository
from src.schemas.inventory_purchase import (
    CreateInventoryPurchaseSchema,
    ResponseInventoryPurchaseSchema,
)
from src.services.base_implementation import BaseServiceImplementation


class InventoryPurchaseService(BaseServiceImplementation):
    def __init__(self):
        super().__init__(
            repository=InventoryPurchaseRepository(),
            model=InventoryPurchaseModel,
            create_schema=CreateInventoryPurchaseSchema,
            response_schema=ResponseInventoryPurchaseSchema,
        )
        self.inventory_item_repository = InventoryItemRepository()

    def add_stock(
        self,
        inventory_item_id: int,
        quantity: float,
        unit_cost: float,
        notes: Optional[str] = None,
    ) -> ResponseInventoryPurchaseSchema:
        """Add stock to an inventory item and record the purchase."""
        inventory_item = self.inventory_item_repository.find(inventory_item_id)

        total_cost = quantity * unit_cost

        purchase = CreateInventoryPurchaseSchema(
            inventory_item_id=inventory_item_id,
            quantity=quantity,
            unit_cost=unit_cost,
            total_cost=total_cost,
            notes=notes,
            purchase_date=datetime.now(),
        )

        new_stock = inventory_item.current_stock + quantity
        self.inventory_item_repository.update(
            inventory_item_id, {"current_stock": new_stock, "purchase_cost": unit_cost}
        )

        return self.save(purchase)
