from src.models.locality import LocalityModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.locality import (
    CreateLocalitySchema,
    ResponseLocalitySchema,
)


class LocalityRepository(BaseRepositoryImplementation):
    """Repositorio para manejar las operaciones de localidad."""

    def __init__(self):
        super().__init__(
            model=LocalityModel,
            create_schema=CreateLocalitySchema,
            response_schema=ResponseLocalitySchema,
        )
