from typing import Any, Dict

from fastapi import Depends

from src.controllers.base_implementation import BaseControllerImplementation
from src.models.user import UserRole
from src.schemas.inventory_item_category import (
    CreateInventoryItemCategorySchema,
    ResponseInventoryItemCategorySchema,
)
from src.schemas.pagination import PaginatedResponseSchema
from src.services.inventory_item_category import InventoryItemCategoryService
from src.utils.rbac import has_role


class InventoryItemCategoryController(BaseControllerImplementation):
    """Controlador para manejar las categorías de artículos de inventario."""

    def __init__(self):
        super().__init__(
            create_schema=CreateInventoryItemCategorySchema,
            response_schema=ResponseInventoryItemCategorySchema,
            service=InventoryItemCategoryService(),
            tags=["Inventory Item Category"],
        )

        @self.router.get("/top-level/all", response_model=PaginatedResponseSchema)
        async def get_top_level_categories(
            offset: int = 0,
            limit: int = 10,
            _: Dict[str, Any] = Depends(
                has_role([UserRole.cocinero, UserRole.administrador])
            ),
        ) -> PaginatedResponseSchema:
            """Obtiene todas las categorías de nivel superior con sus subcategorias."""
            return self.service.get_top_level_categories(offset, limit)
