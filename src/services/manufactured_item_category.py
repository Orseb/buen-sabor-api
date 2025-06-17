from typing import Dict

from src.models.manufactured_item_category import ManufacturedItemCategoryModel
from src.repositories.inventory_item_category import InventoryItemCategoryRepository
from src.repositories.manufactured_item_category import (
    ManufacturedItemCategoryRepository,
)
from src.schemas.manufactured_item_category import (
    CreateManufacturedItemCategorySchema,
    ResponseManufacturedItemCategorySchema,
)
from src.schemas.pagination import PaginatedResponseSchema
from src.services.base_implementation import BaseServiceImplementation


class ManufacturedItemCategoryService(BaseServiceImplementation):
    """Servicio para manejar la lógica de negocio relacionada con las categorías de productos."""

    def __init__(self):
        super().__init__(
            repository=ManufacturedItemCategoryRepository(),
            model=ManufacturedItemCategoryModel,
            create_schema=CreateManufacturedItemCategorySchema,
            response_schema=ResponseManufacturedItemCategorySchema,
        )
        self.inventory_item_category_repository = InventoryItemCategoryRepository()

    def save(
        self, schema: CreateManufacturedItemCategorySchema
    ) -> ResponseManufacturedItemCategorySchema:
        """Guarda una nueva categoría de productos, verificando las reglas de jerarquía."""
        if schema.parent_id:
            parent = self.repository.find(schema.parent_id)
            if parent.parent_id:
                raise ValueError("Las subcategorías no pueden tener subcategorías.")

        return super().save(schema)

    def update(
        self,
        id_key: int,
        schema: CreateManufacturedItemCategorySchema,
    ) -> ResponseManufacturedItemCategorySchema:
        """Actualiza una categoría de productos, verificando las reglas de jerarquía."""
        current_category = self.repository.find(id_key)
        if (
            hasattr(current_category, "subcategories")
            and current_category.subcategories
            and schema.parent_id
        ):
            raise ValueError(
                "Las categorías con subcategorías no pueden convertirse en subcategorias."
            )

        if schema.parent_id:
            if schema.parent_id == id_key:
                raise ValueError("Una categoría no puede ser su propio padre.")

            parent = self.repository.find(schema.parent_id)
            if parent.parent_id:
                raise ValueError("Las subcategorías no pueden tener subcategorías.")

        return super().update(id_key, schema)

    def get_top_level_categories(
        self, offset: int, limit: int
    ) -> PaginatedResponseSchema:
        """Obtiene las categorías de productos de nivel superior con paginación."""
        total = self.repository.count_all_top_level()
        items = self.repository.get_top_level_categories(offset, limit)
        return PaginatedResponseSchema(
            total=total, offset=offset, limit=limit, items=items
        )

    def get_all_public_subcategories(self) -> Dict[str, list]:
        """Obtiene todas las subcategorías de artículos manufacturados e inventario."""
        manufactured_item_subcategories = self.repository.get_all_public_subcategories()
        inventory_subcategories = (
            self.inventory_item_category_repository.get_all_public_subcategories()
        )
        return {
            "manufactured_item_categories": manufactured_item_subcategories,
            "inventory_item_categories": inventory_subcategories,
        }
