from datetime import datetime

from src.models.inventory_purchase import InventoryPurchaseModel
from src.repositories.inventory_item import InventoryItemRepository
from src.repositories.inventory_purchase import InventoryPurchaseRepository
from src.schemas.inventory_purchase import (
    CreateInventoryPurchaseSchema,
    ResponseInventoryPurchaseSchema,
)
from src.services.base_implementation import BaseServiceImplementation


class InventoryPurchaseService(BaseServiceImplementation):
    """Servicio para manejar las compras de inventario."""

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
        purchase_data: CreateInventoryPurchaseSchema,
    ) -> ResponseInventoryPurchaseSchema:
        """Agrega stock a un artículo de inventario."""
        inventory_item = self.inventory_item_repository.find(inventory_item_id)

        if purchase_data.purchase_date is None:
            purchase_data.purchase_date = datetime.now()

        new_stock = inventory_item.current_stock + purchase_data.quantity

        if new_stock < 0:
            raise ValueError("La cantidad de stock no puede ser negativa.")

        if purchase_data.unit_cost <= 0:
            new_inventory_item_cost = inventory_item.purchase_cost
            purchase_data.unit_cost = 0
        else:
            new_inventory_item_cost = purchase_data.unit_cost

        self.inventory_item_repository.update(
            inventory_item_id,
            {"current_stock": new_stock, "purchase_cost": new_inventory_item_cost},
        )
        dict_purchase_data = purchase_data.model_dump(exclude_unset=True)
        dict_purchase_data["inventory_item_id"] = inventory_item_id
        dict_purchase_data["total_cost"] = (
            purchase_data.quantity * purchase_data.unit_cost
        )
        model_purchase_data = self.model(**dict_purchase_data)

        return self.repository.save(model_purchase_data)
