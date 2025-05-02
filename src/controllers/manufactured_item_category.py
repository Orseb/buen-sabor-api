from src.controllers.base_implementation import BaseControllerImplementation
from src.schemas.manufactured_item_category import (
    CreateManufacturedItemCategorySchema,
    ResponseManufacturedItemCategorySchema,
)
from src.services.manufactured_item_category import ManufacturedItemCategoryService


class ManufacturedItemCategoryController(BaseControllerImplementation):
    def __init__(self):
        super().__init__(
            create_schema=CreateManufacturedItemCategorySchema,
            response_schema=ResponseManufacturedItemCategorySchema,
            service=ManufacturedItemCategoryService(),
            tags=["Manufactured Item Category"],
        )
