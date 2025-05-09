from typing import List

from fastapi import Depends, HTTPException, Path

from src.controllers.base_implementation import BaseControllerImplementation
from src.models.user import UserRole
from src.schemas.address import (
    CreateAddressSchema,
    ResponseAddressSchema,
    UpdateAddressSchema,
)
from src.services.address import AddressService
from src.utils.rbac import get_current_user


class AddressController(BaseControllerImplementation):
    def __init__(self):
        super().__init__(
            create_schema=CreateAddressSchema,
            response_schema=ResponseAddressSchema,
            service=AddressService(),
            tags=["Address"],
            required_roles=[UserRole.administrador],
        )

        # Add custom routes for user address management
        @self.router.get("/user/addresses", response_model=List[ResponseAddressSchema])
        async def get_user_addresses(current_user: dict = Depends(get_current_user)):
            """Get all addresses for the current user"""
            user_id = current_user["id"]
            return self.service.get_user_addresses(user_id)

        @self.router.post("/user/addresses", response_model=ResponseAddressSchema)
        async def create_user_address(
            address: UpdateAddressSchema, current_user: dict = Depends(get_current_user)
        ):
            """Create a new address for the current user"""
            user_id = current_user["id"]
            try:
                return self.service.create_user_address(user_id, address)
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

        @self.router.put(
            "/user/addresses/{address_id}", response_model=ResponseAddressSchema
        )
        async def update_user_address(
            address_id: int = Path(...),
            address: UpdateAddressSchema = None,
            current_user: dict = Depends(get_current_user),
        ):
            """Update an address for the current user"""
            user_id = current_user["id"]
            try:
                return self.service.update_user_address(user_id, address_id, address)
            except ValueError as e:
                raise HTTPException(status_code=403, detail=str(e))
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

        @self.router.delete("/user/addresses/{address_id}")
        async def delete_user_address(
            address_id: int = Path(...), current_user: dict = Depends(get_current_user)
        ):
            """Delete an address for the current user"""
            user_id = current_user["id"]
            try:
                self.service.delete_user_address(user_id, address_id)
                return {"message": "Address deleted successfully"}
            except ValueError as e:
                raise HTTPException(status_code=403, detail=str(e))
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))
