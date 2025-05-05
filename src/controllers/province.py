from src.controllers.base_implementation import BaseControllerImplementation
from src.schemas.province import (
    CreateProvinceSchema,
    ResponseProvinceSchema,
)
from src.services.province import ProvinceService


class ProvinceController(BaseControllerImplementation):
    def __init__(self):
        super().__init__(
            create_schema=CreateProvinceSchema,
            response_schema=ResponseProvinceSchema,
            service=ProvinceService(),
            tags=["Province"],
        )
