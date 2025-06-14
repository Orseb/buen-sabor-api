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
        """Save a category with validation for subcategory constraints."""
        if schema.parent_id is not None:
            parent = self.get_one(schema.parent_id)
            if parent.parent_id is not None:
                raise ValueError("Subcategories cannot have their own subcategories")

        return super().save(schema)

    def update(
        self, id_key: int, schema_or_dict
    ) -> ResponseManufacturedItemCategorySchema:
        """Update a category with validation for subcategory constraints."""
        current = self.get_one(id_key)

        if (
            hasattr(current, "subcategories")
            and current.subcategories
            and getattr(schema_or_dict, "parent_id", None) is not None
        ):
            raise ValueError(
                "Categories with subcategories cannot become subcategories"
            )

        parent_id = getattr(schema_or_dict, "parent_id", None)
        if parent_id is not None:
            if parent_id == id_key:
                raise ValueError("A category cannot be its own parent")

            parent = self.get_one(parent_id)
            if parent.parent_id is not None:
                raise ValueError("Subcategories cannot have their own subcategories")

        return super().update(id_key, schema_or_dict)

    def get_top_level_categories(
        self, offset: int, limit: int
    ) -> PaginatedResponseSchema:
        """Get all top-level categories."""
        total = self.repository.count_all_top_level()
        items = self.repository.get_top_level_categories(offset, limit)
        return PaginatedResponseSchema(
            total=total, offset=offset, limit=limit, items=items
        )
