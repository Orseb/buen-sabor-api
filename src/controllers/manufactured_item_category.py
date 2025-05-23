from typing import List

from fastapi import Depends, HTTPException, Path

from src.controllers.base_implementation import BaseControllerImplementation
from src.models.user import UserRole
from src.schemas.manufactured_item_category import (
    CreateManufacturedItemCategorySchema,
    ResponseManufacturedItemCategorySchema,
)
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
            response_model=List[ResponseManufacturedItemCategorySchema],
        )
        async def get_top_level_categories(
            current_user: dict = Depends(
                has_role([UserRole.administrador, UserRole.cajero, UserRole.cocinero])
            )
        ):
            """Get all top-level categories (those without a parent)."""
            return self.service.get_top_level_categories()

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
            try:
                return self.service.get_subcategories(category_id)
            except Exception as e:
                raise HTTPException(status_code=404, detail=str(e))

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
            try:
                return self.service.get_category_with_subcategories(category_id)
            except Exception as e:
                raise HTTPException(status_code=404, detail=str(e))
