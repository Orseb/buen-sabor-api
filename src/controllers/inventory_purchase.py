from fastapi import APIRouter, Depends

from src.models.user import UserRole
from src.schemas.inventory_purchase import (
    CreateInventoryPurchaseSchema,
    ResponseInventoryPurchaseSchema,
)
from src.services.inventory_purchase import InventoryPurchaseService
from src.utils.rbac import has_role


class InventoryPurchaseController:
    """Controlador para manejar las compras de inventario."""

    def __init__(self):
        self.router = APIRouter(tags=["Inventory Purchase"])
        self.service = InventoryPurchaseService()

        @self.router.post(
            "/add-stock/{inventory_item_id}",
            response_model=ResponseInventoryPurchaseSchema,
        )
        async def add_stock(
            inventory_item_id: int,
            purchase_data: CreateInventoryPurchaseSchema,
            _: dict = Depends(has_role([UserRole.administrador, UserRole.cocinero])),
        ) -> ResponseInventoryPurchaseSchema:
            """Agrega stock a un artículo de inventario y crea registro de compra."""
            return self.service.add_stock(inventory_item_id, purchase_data)
