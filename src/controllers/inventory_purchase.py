from datetime import datetime
from typing import List

from fastapi import Depends, Query

from src.controllers.base_implementation import BaseControllerImplementation
from src.models.user import UserRole
from src.schemas.inventory_purchase import (
    CreateInventoryPurchaseSchema,
    ResponseInventoryPurchaseSchema,
)
from src.services.inventory_purchase import InventoryPurchaseService
from src.utils.rbac import has_role


class InventoryPurchaseController(BaseControllerImplementation):
    def __init__(self):
        super().__init__(
            create_schema=CreateInventoryPurchaseSchema,
            response_schema=ResponseInventoryPurchaseSchema,
            service=InventoryPurchaseService(),
            tags=["Inventory Purchase"],
            required_roles=[UserRole.administrador, UserRole.cajero],
        )

        @self.router.post(
            "/add-stock/{inventory_item_id}",
            response_model=ResponseInventoryPurchaseSchema,
        )
        async def add_stock(
            inventory_item_id: int,
            quantity: int = Query(..., gt=0),
            unit_cost: float = Query(..., gt=0),
            notes: str = None,
            current_user: dict = Depends(
                has_role([UserRole.administrador, UserRole.cocinero])
            ),
        ):
            """Add stock to an inventory item and record the purchase."""
            return self.service.add_stock(
                inventory_item_id=inventory_item_id,
                quantity=quantity,
                unit_cost=unit_cost,
                notes=notes,
            )

        @self.router.get(
            "/by-date-range", response_model=List[ResponseInventoryPurchaseSchema]
        )
        async def get_purchases_by_date_range(
            start_date: datetime = Query(...),
            end_date: datetime = Query(...),
            current_user: dict = Depends(
                has_role([UserRole.administrador, UserRole.cajero])
            ),
        ):
            """Get all purchases within a date range."""
            return self.service.get_purchases_by_date_range(start_date, end_date)

        @self.router.get("/expenses")
        async def get_expenses_by_date_range(
            start_date: datetime = Query(...),
            end_date: datetime = Query(...),
            current_user: dict = Depends(
                has_role([UserRole.administrador, UserRole.cajero])
            ),
        ):
            """Calculate total expenses from purchases within a date range."""
            return self.service.get_expenses_by_date_range(start_date, end_date)
