from src.controllers.base_implementation import BaseControllerImplementation
from src.schemas.country import (
    CreateCountrySchema,
    ResponseCountrySchema,
)
from src.services.country import CountryService


class CountryController(BaseControllerImplementation):
    def __init__(self):
        super().__init__(
            create_schema=CreateCountrySchema,
            response_schema=ResponseCountrySchema,
            service=CountryService(),
            tags=["Country"],
        )
