from typing import Any, Dict

from fastapi import Depends, HTTPException

from src.controllers.base_implementation import BaseControllerImplementation
from src.repositories.base_implementation import RecordNotFoundError
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
        )

        @self.router.put(
            "/{id_key}/image", response_model=ResponseManufacturedItemSchema
        )
        def update_manufactured_item_image(
            id_key: int,
            image_base64: str,
            current_user: Dict[str, Any] = Depends(get_current_user),
        ):
            try:
                return self.service.update_image(id_key, image_base64)
            except RecordNotFoundError as error:
                raise HTTPException(status_code=404, detail=str(error))
