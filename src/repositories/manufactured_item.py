from src.models.manufactured_item import ManufacturedItemModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.manufactured_item import (
    CreateManufacturedItemSchema,
    ResponseManufacturedItemSchema,
)


class ManufacturedItemRepository(BaseRepositoryImplementation):
    def __init__(self):
        super().__init__(
            model=ManufacturedItemModel,
            create_schema=CreateManufacturedItemSchema,
            response_schema=ResponseManufacturedItemSchema,
        )
