from typing import List

from fastapi import Depends, Path

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
    def __init__(self):
        super().__init__(
            create_schema=CreateInventoryItemCategorySchema,
            response_schema=ResponseInventoryItemCategorySchema,
            service=InventoryItemCategoryService(),
            tags=["Inventory Item Category"],
        )

        self._register_subcategory_routes()

    def _register_subcategory_routes(self):
        @self.router.get("/top-level/all", response_model=PaginatedResponseSchema)
        async def get_top_level_categories(
            offset: int = 0,
            limit: int = 10,
            current_user: dict = Depends(
                has_role([UserRole.administrador, UserRole.cajero, UserRole.cocinero])
            ),
        ):
            """Get all top-level categories (those without a parent)."""
            return self.service.get_top_level_categories(offset, limit)

        @self.router.get(
            "/{category_id}/subcategories",
            response_model=List[ResponseInventoryItemCategorySchema],
        )
        async def get_subcategories(
            category_id: int = Path(...),
            current_user: dict = Depends(
                has_role([UserRole.administrador, UserRole.cajero, UserRole.cocinero])
            ),
        ):
            """Get all subcategories for a given parent category."""
            return self.service.get_subcategories(category_id)

        @self.router.get(
            "/{category_id}/with-subcategories",
            response_model=ResponseInventoryItemCategorySchema,
        )
        async def get_category_with_subcategories(
            category_id: int = Path(...),
            current_user: dict = Depends(
                has_role([UserRole.administrador, UserRole.cajero, UserRole.cocinero])
            ),
        ):
            """Get a category with its subcategories."""
            return self.service.get_category_with_subcategories(category_id)
