from typing import List

from fastapi import Depends, Path

from src.controllers.base_implementation import BaseControllerImplementation
from src.models.user import UserRole
from src.schemas.manufactured_item_category import (
    CreateManufacturedItemCategorySchema,
    ResponseManufacturedItemCategorySchema,
)
from src.schemas.pagination import PaginatedResponseSchema
from src.services.manufactured_item_category import ManufacturedItemCategoryService
from src.utils.rbac import has_role


class ManufacturedItemCategoryController(BaseControllerImplementation):
    def __init__(self):
        super().__init__(
            create_schema=CreateManufacturedItemCategorySchema,
            response_schema=ResponseManufacturedItemCategorySchema,
            service=ManufacturedItemCategoryService(),
            tags=["Manufactured Item Category"],
        )

        self._register_subcategory_routes()

    def _register_subcategory_routes(self):
        @self.router.get(
            "/top-level/all",
            response_model=PaginatedResponseSchema,
        )
        async def get_top_level_categories(
            offset: int = 0,
            limit: int = 10,
            current_user: dict = Depends(
                has_role([UserRole.administrador, UserRole.cajero, UserRole.cocinero])
            ),
        ):
            """Get all top-level categories."""
            return self.service.get_top_level_categories(offset, limit)

        @self.router.get(
            "/{category_id}/subcategories",
            response_model=List[ResponseManufacturedItemCategorySchema],
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
            response_model=ResponseManufacturedItemCategorySchema,
        )
        async def get_category_with_subcategories(
            category_id: int = Path(...),
            current_user: dict = Depends(
                has_role([UserRole.administrador, UserRole.cajero, UserRole.cocinero])
            ),
        ):
            """Get a category with its subcategories."""
            return self.service.get_category_with_subcategories(category_id)
