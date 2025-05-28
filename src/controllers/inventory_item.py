from typing import Any, Dict, List

from fastapi import Depends, HTTPException

from src.controllers.base_implementation import BaseControllerImplementation
from src.repositories.base_implementation import RecordNotFoundError
from src.schemas.inventory_item import (
    CreateInventoryItemSchema,
    ResponseInventoryItemSchema,
)
from src.services.inventory_item import InventoryItemService
from src.utils.rbac import get_current_user


class InventoryItemController(BaseControllerImplementation):
    def __init__(self):
        super().__init__(
            create_schema=CreateInventoryItemSchema,
            response_schema=ResponseInventoryItemSchema,
            service=InventoryItemService(),
            tags=["Inventory Item"],
        )

        @self.router.get(
            "/products/all", response_model=List[ResponseInventoryItemSchema]
        )
        def get_product_inventory_items(
            current_user: Dict[str, Any] = Depends(get_current_user),
        ):
            return self.service.get_all_by("is_ingredient", False)

        @self.router.put("/{id_key}/image", response_model=ResponseInventoryItemSchema)
        def update_inventory_item_image(
            id_key: int,
            image_base64: str,
            current_user: Dict[str, Any] = Depends(get_current_user),
        ):
            try:
                return self.service.update_image(id_key, image_base64)
            except RecordNotFoundError as error:
                raise HTTPException(status_code=404, detail=str(error))
