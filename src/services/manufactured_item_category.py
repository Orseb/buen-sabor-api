from typing import Any

from src.models.manufactured_item_category import ManufacturedItemCategoryModel
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
        schema_or_dict: CreateManufacturedItemCategorySchema | dict[str, Any],
    ) -> ResponseManufacturedItemCategorySchema:
        """Actualiza una categoría de productos, verificando las reglas de jerarquía."""
        current_category = self.repository.find(id_key)
        if (
            hasattr(current_category, "subcategories")
            and current_category.subcategories
            and getattr(schema_or_dict, "parent_id", None)
        ):
            raise ValueError(
                "Las categorías con subcategorías no pueden convertirse en subcategorias."
            )

        parent_id = getattr(schema_or_dict, "parent_id", None)
        if parent_id:
            if parent_id == id_key:
                raise ValueError("Una categoría no puede ser su propio padre.")

            parent = self.repository.find(parent_id)
            if parent.parent_id:
                raise ValueError("Las subcategorías no pueden tener subcategorías.")

        return super().update(id_key, schema_or_dict)

    def get_top_level_categories(
        self, offset: int, limit: int
    ) -> PaginatedResponseSchema:
        """Obtiene las categorías de productos de nivel superior con paginación."""
        total = self.repository.count_all_top_level()
        items = self.repository.get_top_level_categories(offset, limit)
        return PaginatedResponseSchema(
            total=total, offset=offset, limit=limit, items=items
        )
