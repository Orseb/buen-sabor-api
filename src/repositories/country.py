from src.models.country import CountryModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.country import (
    CreateCountrySchema,
    ResponseCountrySchema,
)


class CountryRepository(BaseRepositoryImplementation):
    def __init__(self):
        super().__init__(
            model=CountryModel,
            create_schema=CreateCountrySchema,
            response_schema=ResponseCountrySchema,
        )
