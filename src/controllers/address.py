from fastapi import APIRouter, Depends, Path

from src.schemas.address import (
    CreateAddressSchema,
    ResponseAddressSchema,
)
from src.schemas.pagination import PaginatedResponseSchema
from src.services.address import AddressService
from src.utils.rbac import get_current_user


class AddressController:
    """Controlador para manejar las direcciones de los usuarios"""

    def __init__(self):
        """Inicializa el controlador de direcciones"""
        self.router = APIRouter(tags=["Address"])
        self.service = AddressService()

        @self.router.get("/user/addresses", response_model=PaginatedResponseSchema)
        async def get_user_addresses(
            offset: int = 0,
            limit: int = 10,
            current_user: dict = Depends(get_current_user),
        ) -> PaginatedResponseSchema:
            """Obtiene todas las direcciones del usuario actual"""
            return self.service.get_all_by("user_id", current_user["id"], offset, limit)

        @self.router.post("/user/addresses", response_model=ResponseAddressSchema)
        async def create_user_address(
            address: CreateAddressSchema, current_user: dict = Depends(get_current_user)
        ) -> ResponseAddressSchema:
            """Crea una nueva dirección para el usuario actual"""
            return self.service.create_user_address(current_user["id"], address)

        @self.router.put(
            "/user/addresses/{address_id}", response_model=ResponseAddressSchema
        )
        async def update_user_address(
            address_id: int = Path(...),
            address: CreateAddressSchema = None,
            current_user: dict = Depends(get_current_user),
        ) -> ResponseAddressSchema:
            """Actualiza una dirección del usuario actual"""
            return self.service.update_user_address(
                current_user["id"], address_id, address
            )

        @self.router.delete("/user/addresses/{address_id}")
        async def delete_user_address(
            address_id: int = Path(...), current_user: dict = Depends(get_current_user)
        ) -> ResponseAddressSchema:
            """Elimina una dirección del usuario actual"""
            return self.service.delete_user_address(current_user["id"], address_id)
