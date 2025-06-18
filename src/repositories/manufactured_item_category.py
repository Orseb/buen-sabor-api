from sqlalchemy import func, select

from src.models.manufactured_item_category import ManufacturedItemCategoryModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.manufactured_item_category import (
    CreateManufacturedItemCategorySchema,
    ResponseManufacturedItemCategorySchema,
    ResponsePublicManufacturedItemCategorySchema,
)


class ManufacturedItemCategoryRepository(BaseRepositoryImplementation):
    """Repositoriorio para manejar las categorías de artículos manufacturados."""

    def __init__(self):
        super().__init__(
            model=ManufacturedItemCategoryModel,
            create_schema=CreateManufacturedItemCategorySchema,
            response_schema=ResponseManufacturedItemCategorySchema,
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
    ) -> list[ResponseManufacturedItemCategorySchema]:
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
    ) -> list[ResponsePublicManufacturedItemCategorySchema]:
        """Obtiene todas las subcategorías de artículos de inventario."""
        with self.session_scope() as session:
            stmt = select(self.model).where(
                self.model.parent_id.is_not(None), self.model.active.is_(True)
            )

            result = session.execute(stmt)
            return [
                ResponsePublicManufacturedItemCategorySchema.model_validate(category)
                for category in result.scalars()
            ]
