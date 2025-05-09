from typing import List

from src.models.address import AddressModel
from src.repositories.address import AddressRepository
from src.schemas.address import (
    CreateAddressSchema,
    ResponseAddressSchema,
    UpdateAddressSchema,
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

    def get_user_addresses(self, user_id: int) -> List[ResponseAddressSchema]:
        """Get all addresses for a user"""
        with self.repository.session_scope() as session:
            addresses = (
                session.query(self.model).filter(self.model.user_id == user_id).all()
            )
            return [
                self.response_schema.model_validate(address) for address in addresses
            ]

    def create_user_address(
        self, user_id: int, address: UpdateAddressSchema
    ) -> ResponseAddressSchema:
        """Create a new address for a user"""
        create_schema = CreateAddressSchema(**address.model_dump(), user_id=user_id)
        return self.save(create_schema)

    def update_user_address(
        self, user_id: int, address_id: int, address: UpdateAddressSchema
    ) -> ResponseAddressSchema:
        """Update an address for a user"""
        # First verify the address belongs to the user
        existing_address = self.get_one(address_id)
        if existing_address.user_id != user_id:
            raise ValueError("Address does not belong to the user")

        return self.update(address_id, address)

    def delete_user_address(self, user_id: int, address_id: int) -> BaseSchema:
        """Delete an address for a user"""
        # First verify the address belongs to the user
        existing_address = self.get_one(address_id)
        if existing_address.user_id != user_id:
            raise ValueError("Address does not belong to the user")

        return self.delete(address_id)
