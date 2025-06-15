from src.models.address import AddressModel
from src.repositories.address import AddressRepository
from src.schemas.address import (
    CreateAddressSchema,
    ResponseAddressSchema,
)
from src.schemas.base import BaseSchema
from src.services.base_implementation import BaseServiceImplementation


class AddressService(BaseServiceImplementation):
    """Servicio para manejar las direcciones de los usuarios"""

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
        """Crea una dirección para un usuario específico"""
        address.user_id = user_id
        return self.repository.save(address)

    def update_user_address(
        self, user_id: int, address_id: int, address: CreateAddressSchema
    ) -> ResponseAddressSchema:
        """Actualiza una dirección de un usuario específico"""
        self.validate_address_ownership(address_id, user_id)
        return self.repository.update(address_id, address)

    def delete_user_address(self, user_id: int, address_id: int) -> BaseSchema:
        """Elimina una dirección de un usuario específico"""
        self.validate_address_ownership(address_id, user_id)
        return self.repository.remove(address_id)

    def validate_address_ownership(self, address_id: int, user_id: int) -> None:
        """Valida que la dirección pertenece al usuario"""
        address = self.get_one(address_id)
        if address.user_id != user_id:
            raise ValueError("La dirección no pertenece al usuario especificado")
