from src.models.manufactured_item_category import ManufacturedItemCategoryModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.manufactured_item_category import (
    CreateManufacturedItemCategorySchema,
    ResponseManufacturedItemCategorySchema,
)


class ManufacturedItemCategoryRepository(BaseRepositoryImplementation):
    def __init__(self):
        super().__init__(
            model=ManufacturedItemCategoryModel,
            create_schema=CreateManufacturedItemCategorySchema,
            response_schema=ResponseManufacturedItemCategorySchema,
        )

    def count_all_top_level(self) -> int:
        with self.session_scope() as session:
            return (
                session.query(self.model)
                .filter(self.model.parent_id.is_(None))
                .filter(self.model.active.is_(True))
                .count()
            )

    def get_top_level_categories(
        self, offset, limit
    ) -> list[ResponseManufacturedItemCategorySchema]:
        """Retrieve all top-level categories."""
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
