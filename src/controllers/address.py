from src.controllers.base_implementation import BaseControllerImplementation
from src.schemas.address import (
    CreateAddressSchema,
    ResponseAddressSchema,
)
from src.services.address import AddressService


class AddressController(BaseControllerImplementation):
    def __init__(self):
        super().__init__(
            create_schema=CreateAddressSchema,
            response_schema=ResponseAddressSchema,
            service=AddressService(),
            tags=["Address"],
        )
