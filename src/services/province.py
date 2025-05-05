from src.models.province import ProvinceModel
from src.repositories.province import ProvinceRepository
from src.schemas.province import (
    CreateProvinceSchema,
    ResponseProvinceSchema,
)
from src.services.base_implementation import BaseServiceImplementation


class ProvinceService(BaseServiceImplementation):

    def __init__(self):
        super().__init__(
            repository=ProvinceRepository(),
            model=ProvinceModel,
            create_schema=CreateProvinceSchema,
            response_schema=ResponseProvinceSchema,
        )
