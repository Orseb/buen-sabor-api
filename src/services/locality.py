from src.models.locality import LocalityModel
from src.repositories.locality import LocalityRepository
from src.schemas.locality import (
    CreateLocalitySchema,
    ResponseLocalitySchema,
)
from src.services.base_implementation import BaseServiceImplementation


class LocalityService(BaseServiceImplementation):

    def __init__(self):
        super().__init__(
            repository=LocalityRepository(),
            model=LocalityModel,
            create_schema=CreateLocalitySchema,
            response_schema=ResponseLocalitySchema,
        )
