from src.models.address import AddressModel
from src.repositories.address import AddressRepository
from src.schemas.address import (
    CreateAddressSchema,
    ResponseAddressSchema,
)
from src.schemas.base import BaseSchema
from src.services.base_implementation import BaseServiceImplementation


class AddressService(BaseServiceImplementation):

    def __init__(self):
        super().__init__(
            repository=AddressRepository(),
            model=AddressModel,
            create_schema=CreateAddressSchema,
            response_schema=ResponseAddressSchema,
        )

    def create_user_address(
        self, user_id: int, address: CreateAddressSchema
    ) -> ResponseAddressSchema:
        """Create a new address for a user"""
        create_schema = CreateAddressSchema(**address.model_dump(), user_id=user_id)
        return self.save(create_schema)

    def update_user_address(
        self, user_id: int, address_id: int, address: CreateAddressSchema
    ) -> ResponseAddressSchema:
        """Update an address for a user"""
        self.validate_address_ownership(address_id, user_id)
        return self.update(address_id, address)

    def delete_user_address(self, user_id: int, address_id: int) -> BaseSchema:
        """Delete an address for a user"""
        self.validate_address_ownership(address_id, user_id)
        return self.delete(address_id)

    def validate_address_ownership(self, address_id: int, user_id: int) -> None:
        address = self.get_one(address_id)
        if address.user_id != user_id:
            raise ValueError("Address does not belong to the user")
