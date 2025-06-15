from src.models.address import AddressModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.address import (
    CreateAddressSchema,
    ResponseAddressSchema,
)


class AddressRepository(BaseRepositoryImplementation):
    """Repositorio para manejo de direcciones."""

    def __init__(self):
        super().__init__(
            model=AddressModel,
            create_schema=CreateAddressSchema,
            response_schema=ResponseAddressSchema,
        )
