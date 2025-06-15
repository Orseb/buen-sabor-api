from src.models.inventory_item_category import InventoryItemCategoryModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.inventory_item_category import (
    CreateInventoryItemCategorySchema,
    ResponseInventoryItemCategorySchema,
)


class InventoryItemCategoryRepository(BaseRepositoryImplementation):
    """Repositorio para manejo de categorías de artículos de inventario."""

    def __init__(self):
        super().__init__(
            model=InventoryItemCategoryModel,
            create_schema=CreateInventoryItemCategorySchema,
            response_schema=ResponseInventoryItemCategorySchema,
        )

    def count_all_top_level(self) -> int:
        """Cuenta todas las categorías de nivel superior activas."""
        with self.session_scope() as session:
            return (
                session.query(self.model)
                .filter(self.model.parent_id.is_(None))
                .filter(self.model.active.is_(True))
                .count()
            )

    def get_top_level_categories(
        self, offset: int, limit: int
    ) -> list[ResponseInventoryItemCategorySchema]:
        """Obtiene todas las categorías de nivel superior activas con paginación."""
        with self.session_scope() as session:
            categories = (
                session.query(self.model)
                .filter(self.model.parent_id.is_(None))
                .filter(self.model.active.is_(True))
                .offset(offset)
                .limit(limit)
                .all()
            )
            return [self.schema.model_validate(category) for category in categories]
