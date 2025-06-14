from typing import Any, Dict

from fastapi import Depends

from src.controllers.base_implementation import BaseControllerImplementation
from src.models.user import UserRole
from src.schemas.inventory_item import (
    CreateInventoryItemSchema,
    ResponseInventoryItemSchema,
)
from src.schemas.pagination import PaginatedResponseSchema
from src.services.inventory_item import InventoryItemService
from src.utils.rbac import has_role


class InventoryItemController(BaseControllerImplementation):
    """Controlar para manejar los items del inventario."""

    def __init__(self):
        super().__init__(
            create_schema=CreateInventoryItemSchema,
            response_schema=ResponseInventoryItemSchema,
            service=InventoryItemService(),
            tags=["Inventory Item"],
        )

        @self.router.get("/products/all", response_model=PaginatedResponseSchema)
        def get_product_inventory_items(
            offset: int = 0, limit: int = 10
        ) -> PaginatedResponseSchema:
            """Obtiene todos los items del inventario que no son ingredientes."""
            return self.service.get_all_by("is_ingredient", False, offset, limit)

        @self.router.get("/ingredients/all", response_model=PaginatedResponseSchema)
        def get_ingredient_inventory_items(
            offset: int = 0,
            limit: int = 10,
            _: Dict[str, Any] = Depends(
                has_role([UserRole.administrador, UserRole.cocinero])
            ),
        ) -> PaginatedResponseSchema:
            """Obtiene todos los items del inventario que son ingredientes."""
            return self.service.get_all_by("is_ingredient", True, offset, limit)
