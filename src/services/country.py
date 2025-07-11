from src.models.country import CountryModel
from src.repositories.country import CountryRepository
from src.schemas.country import (
    CreateCountrySchema,
    ResponseCountrySchema,
)
from src.services.base_implementation import BaseServiceImplementation


class CountryService(BaseServiceImplementation):
    """Servicio para manejar la lógica de negocio relacionada con los países."""

    def __init__(self):
        super().__init__(
            repository=CountryRepository(),
            model=CountryModel,
            create_schema=CreateCountrySchema,
            response_schema=ResponseCountrySchema,
        )
