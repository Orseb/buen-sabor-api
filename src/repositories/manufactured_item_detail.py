from src.models.manufactured_item_detail import ManufacturedItemDetailModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.manufactured_item_detail import (
    CreateManufacturedItemDetailSchema,
    ResponseManufacturedItemDetailSchema,
)


class ManufacturedItemDetailRepository(BaseRepositoryImplementation):
    def __init__(self):
        super().__init__(
            model=ManufacturedItemDetailModel,
            create_schema=CreateManufacturedItemDetailSchema,
            response_schema=ResponseManufacturedItemDetailSchema,
        )
