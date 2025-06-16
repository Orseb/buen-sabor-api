from src.models.manufactured_item_category import ManufacturedItemCategoryModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.manufactured_item_category import (
    CreateManufacturedItemCategorySchema,
    ResponseManufacturedItemCategorySchema,
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
            return (
                session.query(self.model)
                .filter(self.model.parent_id.is_(None))
                .filter(self.model.active.is_(True))
                .count()
            )

    def get_top_level_categories(
        self, offset: int, limit: int
    ) -> list[ResponseManufacturedItemCategorySchema]:
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

    def get_all_public_subcategories(
        self,
    ) -> list[ResponseManufacturedItemCategorySchema]:
        """Obtiene todas las subcategorías de artículos manufacturados."""
        with self.session_scope() as session:
            manufactured_categories = (
                session.query(self.model)
                .filter(self.model.parent_id.is_not(None))
                .filter(self.model.active.is_(True))
                .all()
            )
            return [
                self.schema.model_validate(category)
                for category in manufactured_categories
            ]
