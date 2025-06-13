from datetime import datetime
from typing import Dict, List, Optional

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

    def get_purchases_by_date_range(
        self, start_date: datetime, end_date: datetime
    ) -> List[ResponseInventoryPurchaseSchema]:
        """Get all purchases within a date range."""
        with self.repository.session_scope() as session:
            purchases = (
                session.query(self.model)
                .filter(
                    self.model.purchase_date >= start_date,
                    self.model.purchase_date <= end_date,
                )
                .all()
            )

            return [self.schema.model_validate(purchase) for purchase in purchases]

    def get_expenses_by_date_range(
        self, start_date: datetime, end_date: datetime
    ) -> Dict:
        """Calculate total expenses from purchases within a date range."""
        purchases = self.get_purchases_by_date_range(start_date, end_date)

        total_expenses = sum(purchase.total_cost for purchase in purchases)
        purchase_count = len(purchases)

        return {
            "total_expenses": total_expenses,
            "purchase_count": purchase_count,
            "start_date": start_date,
            "end_date": end_date,
        }
