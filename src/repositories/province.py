from src.models.province import ProvinceModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.province import (
    CreateProvinceSchema,
    ResponseProvinceSchema,
)


class ProvinceRepository(BaseRepositoryImplementation):
    def __init__(self):
        super().__init__(
            model=ProvinceModel,
            create_schema=CreateProvinceSchema,
            response_schema=ResponseProvinceSchema,
        )
