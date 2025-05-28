from typing import List

from fastapi import Depends, HTTPException, Path
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

from src.controllers.base_implementation import BaseControllerImplementation
from src.repositories.base_implementation import RecordNotFoundError
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
        )

        @self.router.get("/user/addresses", response_model=List[ResponseAddressSchema])
        async def get_user_addresses(
            offset: int = 0,
            limit: int = 10,
            current_user: dict = Depends(get_current_user),
        ):
            return self.service.get_user_addresses(offset, limit, current_user["id"])

        @self.router.post("/user/addresses", response_model=ResponseAddressSchema)
        async def create_user_address(
            address: UpdateAddressSchema, current_user: dict = Depends(get_current_user)
        ):
            try:
                return self.service.create_user_address(current_user["id"], address)
            except IntegrityError as error:
                if isinstance(error.orig, UniqueViolation):
                    raise HTTPException(
                        status_code=400, detail="Unique constraint violated."
                    )
                raise HTTPException(
                    status_code=500, detail="An unexpected database error occurred."
                )

        @self.router.put(
            "/user/addresses/{address_id}", response_model=ResponseAddressSchema
        )
        async def update_user_address(
            address_id: int = Path(...),
            address: UpdateAddressSchema = None,
            current_user: dict = Depends(get_current_user),
        ):
            try:
                return self.service.update_user_address(
                    current_user["id"], address_id, address
                )
            except RecordNotFoundError as error:
                raise HTTPException(status_code=404, detail=str(error))
            except IntegrityError as error:
                if isinstance(error.orig, UniqueViolation):
                    raise HTTPException(
                        status_code=400, detail="Unique constraint violated."
                    )
                raise HTTPException(
                    status_code=500, detail="An unexpected database error occurred."
                )

        @self.router.delete("/user/addresses/{address_id}")
        async def delete_user_address(
            address_id: int = Path(...), current_user: dict = Depends(get_current_user)
        ):
            try:
                return self.service.delete_user_address(current_user["id"], address_id)
            except RecordNotFoundError as error:
                raise HTTPException(status_code=404, detail=str(error))
