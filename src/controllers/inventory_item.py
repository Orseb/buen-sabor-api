from typing import Any, Dict

from fastapi import Depends

from src.controllers.base_implementation import BaseControllerImplementation
from src.schemas.inventory_item import (
    CreateInventoryItemSchema,
    ResponseInventoryItemSchema,
)
from src.schemas.pagination import PaginatedResponseSchema
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

        @self.router.get("/products/all", response_model=PaginatedResponseSchema)
        def get_product_inventory_items(offset: int = 0, limit: int = 10):
            return self.service.get_all_by("is_ingredient", False, offset, limit)

        @self.router.get("/ingredients/all", response_model=PaginatedResponseSchema)
        def get_ingredient_inventory_items(
            offset: int = 0,
            limit: int = 10,
            current_user: Dict[str, Any] = Depends(get_current_user),
        ):
            return self.service.get_all_by("is_ingredient", True, offset, limit)

        @self.router.put("/{id_key}/image", response_model=ResponseInventoryItemSchema)
        def update_inventory_item_image(
            id_key: int,
            image_base64: str,
            current_user: Dict[str, Any] = Depends(get_current_user),
        ):
            return self.service.update_image(id_key, image_base64)
