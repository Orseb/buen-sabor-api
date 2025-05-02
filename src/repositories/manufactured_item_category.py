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
