from src.models.address import AddressModel
from src.repositories.address import AddressRepository
from src.schemas.address import (
    CreateAddressSchema,
    ResponseAddressSchema,
    UpdateAddressSchema,
)
from src.schemas.base import BaseSchema
from src.schemas.pagination import PaginatedResponseSchema
from src.services.base_implementation import BaseServiceImplementation


class AddressService(BaseServiceImplementation):

    def __init__(self):
        super().__init__(
            repository=AddressRepository(),
            model=AddressModel,
            create_schema=CreateAddressSchema,
            response_schema=ResponseAddressSchema,
        )

    def get_user_addresses(
        self, offset: int, limit: int, user_id: int
    ) -> PaginatedResponseSchema:
        """Get all addresses for a user"""
        total = self.repository.count_all_user_addresses(user_id)
        items = self.repository.get_user_addresses(user_id, offset, limit)
        return PaginatedResponseSchema(
            total=total, offset=offset, limit=limit, items=items
        )

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
        existing_address = self.get_one(address_id)
        if existing_address.user_id != user_id:
            raise ValueError("Address does not belong to the user")

        return self.update(address_id, address)

    def delete_user_address(self, user_id: int, address_id: int) -> BaseSchema:
        """Delete an address for a user"""
        existing_address = self.get_one(address_id)
        if existing_address.user_id != user_id:
            raise ValueError("Address does not belong to the user")

        return self.delete(address_id)
