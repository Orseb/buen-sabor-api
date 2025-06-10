from fastapi import Depends, Path

from src.controllers.base_implementation import BaseControllerImplementation
from src.schemas.address import (
    CreateAddressSchema,
    ResponseAddressSchema,
    UpdateAddressSchema,
)
from src.schemas.pagination import PaginatedResponseSchema
from src.services.address import AddressService
from src.utils.rbac import get_current_user


class AddressController(BaseControllerImplementation):
    def __init__(self):
        super().__init__(
            create_schema=CreateAddressSchema,
            response_schema=ResponseAddressSchema,
            service=AddressService(),
            tags=["Address"],
        )

        @self.router.get("/user/addresses", response_model=PaginatedResponseSchema)
        async def get_user_addresses(
            offset: int = 0,
            limit: int = 10,
            current_user: dict = Depends(get_current_user),
        ):
            return self.service.get_all_by("user_id", current_user["id"], offset, limit)

        @self.router.post("/user/addresses", response_model=ResponseAddressSchema)
        async def create_user_address(
            address: UpdateAddressSchema, current_user: dict = Depends(get_current_user)
        ):
            return self.service.create_user_address(current_user["id"], address)

        @self.router.put(
            "/user/addresses/{address_id}", response_model=ResponseAddressSchema
        )
        async def update_user_address(
            address_id: int = Path(...),
            address: UpdateAddressSchema = None,
            current_user: dict = Depends(get_current_user),
        ):
            return self.service.update_user_address(
                current_user["id"], address_id, address
            )

        @self.router.delete("/user/addresses/{address_id}")
        async def delete_user_address(
            address_id: int = Path(...), current_user: dict = Depends(get_current_user)
        ):
            return self.service.delete_user_address(current_user["id"], address_id)
