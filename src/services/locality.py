from src.models.locality import LocalityModel
from src.repositories.locality import LocalityRepository
from src.schemas.locality import (
    CreateLocalitySchema,
    ResponseLocalitySchema,
)
from src.services.base_implementation import BaseServiceImplementation


class LocalityService(BaseServiceImplementation):
    """Servicio para manejar la lógica de negocio relacionada con las localidades."""

    def __init__(self):
        super().__init__(
            repository=LocalityRepository(),
            model=LocalityModel,
            create_schema=CreateLocalitySchema,
            response_schema=ResponseLocalitySchema,
        )
