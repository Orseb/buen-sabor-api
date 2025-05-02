from src.models.manufactured_item_category import ManufacturedItemCategoryModel
from src.repositories.manufactured_item_category import (
    ManufacturedItemCategoryRepository,
)
from src.schemas.manufactured_item_category import (
    CreateManufacturedItemCategorySchema,
    ResponseManufacturedItemCategorySchema,
)
from src.services.base_implementation import BaseServiceImplementation


class ManufacturedItemCategoryService(BaseServiceImplementation):

    def __init__(self):
        super().__init__(
            repository=ManufacturedItemCategoryRepository(),
            model=ManufacturedItemCategoryModel,
            create_schema=CreateManufacturedItemCategorySchema,
            response_schema=ResponseManufacturedItemCategorySchema,
        )
