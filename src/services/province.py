from src.models.province import ProvinceModel
from src.repositories.province import ProvinceRepository
from src.schemas.province import (
    CreateProvinceSchema,
    ResponseProvinceSchema,
)
from src.services.base_implementation import BaseServiceImplementation


class ProvinceService(BaseServiceImplementation):
    """Servicio para manejar la lógica de negocio relacionada con las provincias."""

    def __init__(self):
        super().__init__(
            repository=ProvinceRepository(),
            model=ProvinceModel,
            create_schema=CreateProvinceSchema,
            response_schema=ResponseProvinceSchema,
        )
