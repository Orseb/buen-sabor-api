from typing import List

from fastapi import Query

from src.controllers.base_implementation import BaseControllerImplementation
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
        )

        @self.router.get(
            "/category/{category_id}",
            response_model=List[ResponseManufacturedItemSchema],
        )
        async def get_by_category(category_id: int):
            return self.service.get_by_category(category_id)

        @self.router.get("/search", response_model=List[ResponseManufacturedItemSchema])
        async def search_by_name(name: str = Query(...)):
            return self.service.search_by_name(name)

        @self.router.get("/check-stock/{id_key}")
        async def check_stock(id_key: int, quantity: int = Query(1)):
            available = self.service.check_stock_availability(id_key, quantity)
            max_quantity = self.service.get_max_quantity_available(id_key)
            return {
                "available": available,
                "max_quantity": max_quantity,
            }
