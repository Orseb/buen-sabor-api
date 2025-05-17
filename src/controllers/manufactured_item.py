from src.controllers.base_implementation import BaseControllerImplementation
from src.models.user import UserRole
from src.schemas.manufactured_item import (
    CreateManufacturedItemSchema,
    ResponseManufacturedItemSchema,
)
from src.services.manufactured_item import ManufacturedItemService


class ManufacturedItemController(BaseControllerImplementation):
    def __init__(self):
        super().__init__(
            create_schema=CreateManufacturedItemSchema,
            response_schema=ResponseManufacturedItemSchema,
            service=ManufacturedItemService(),
            tags=["Manufactured Item"],
            required_roles=[
                UserRole.administrador,
                UserRole.cajero,
                UserRole.delivery,
                UserRole.cocinero,
                UserRole.cliente,
            ],
        )
