from src.models.address import AddressModel
from src.repositories.address import AddressRepository
from src.schemas.address import (
    CreateAddressSchema,
    ResponseAddressSchema,
)
from src.services.base_implementation import BaseServiceImplementation


class AddressService(BaseServiceImplementation):

    def __init__(self):
        super().__init__(
            repository=AddressRepository(),
            model=AddressModel,
            create_schema=CreateAddressSchema,
            response_schema=ResponseAddressSchema,
        )
