from sqlalchemy import func, select

from src.models.inventory_item_category import InventoryItemCategoryModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.inventory_item_category import (
    CreateInventoryItemCategorySchema,
    ResponseInventoryItemCategorySchema,
    ResponsePublicInventoryItemCategorySchema,
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
            stmt = select(func.count()).where(
                self.model.parent_id.is_(None), self.model.active.is_(True)
            )
            return session.scalar(stmt)

    def get_top_level_categories(
        self, offset: int, limit: int
    ) -> list[ResponseInventoryItemCategorySchema]:
        """Obtiene todas las categorías de nivel superior activas con paginación."""
        with self.session_scope() as session:
            stmt = (
                select(self.model)
                .where(self.model.parent_id.is_(None), self.model.active.is_(True))
                .offset(offset)
                .limit(limit)
            )

            result = session.execute(stmt)
            return [
                self.schema.model_validate(category) for category in result.scalars()
            ]

    def get_all_public_subcategories(
        self,
    ) -> list[ResponsePublicInventoryItemCategorySchema]:
        """Obtiene todas las subcategorías de artículos de inventario."""
        with self.session_scope() as session:
            stmt = select(self.model).where(
                self.model.parent_id.is_not(None),
                self.model.active.is_(True),
                self.model.public.is_(True),
            )

            result = session.execute(stmt)
            return [
                ResponsePublicInventoryItemCategorySchema.model_validate(category)
                for category in result.scalars()
            ]
