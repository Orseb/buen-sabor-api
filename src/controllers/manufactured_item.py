from fastapi import Depends

from src.controllers.base_implementation import BaseControllerImplementation
from src.schemas.manufactured_item import (
    CreateManufacturedItemSchema,
    ResponseManufacturedItemSchema,
)
from src.services.manufactured_item import ManufacturedItemService
from src.utils.rbac import get_current_user


class ManufacturedItemController(BaseControllerImplementation):
    def __init__(self):
        super().__init__(
            create_schema=CreateManufacturedItemSchema,
            response_schema=ResponseManufacturedItemSchema,
            service=ManufacturedItemService(),
            tags=["Manufactured Item"],
            required_roles=Depends(get_current_user),
        )
