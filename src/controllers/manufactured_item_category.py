from src.controllers.base_implementation import BaseControllerImplementation
from src.schemas.manufactured_item_category import (
    CreateManufacturedItemCategorySchema,
    ResponseManufacturedItemCategorySchema,
)
from src.schemas.pagination import PaginatedResponseSchema
from src.services.manufactured_item_category import ManufacturedItemCategoryService


class ManufacturedItemCategoryController(BaseControllerImplementation):
    """Controlador para manejar las categorías de artículos manufacturados."""

    def __init__(self):
        super().__init__(
            create_schema=CreateManufacturedItemCategorySchema,
            response_schema=ResponseManufacturedItemCategorySchema,
            service=ManufacturedItemCategoryService(),
            tags=["Manufactured Item Category"],
        )

        @self.router.get(
            "/top-level/all",
            response_model=PaginatedResponseSchema,
        )
        async def get_top_level_categories(
            offset: int = 0, limit: int = 10
        ) -> PaginatedResponseSchema:
            """Obtiene todas las categorías de artículos manufacturados de nivel superior."""
            return self.service.get_top_level_categories(offset, limit)

        @self.router.get("/public-subcategories/all")
        async def get_all_public_subcategories() -> dict:
            """Obtiene todas las subcategorías de artículos manufacturados e inventario."""
            return self.service.get_all_public_subcategories()
