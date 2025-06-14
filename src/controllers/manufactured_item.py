from src.controllers.base_implementation import BaseControllerImplementation
from src.schemas.manufactured_item import (
    CreateManufacturedItemSchema,
    ResponseManufacturedItemSchema,
)
from src.schemas.pagination import PaginatedResponseSchema
from src.services.manufactured_item import ManufacturedItemService


class ManufacturedItemController(BaseControllerImplementation):
    def __init__(self):
        super().__init__(
            create_schema=CreateManufacturedItemSchema,
            response_schema=ResponseManufacturedItemSchema,
            service=ManufacturedItemService(),
            tags=["Manufactured Item"],
        )

        @self.router.get("/products/all", response_model=PaginatedResponseSchema)
        def get_product_inventory_items(offset: int = 0, limit: int = 10):
            """Get manufactured items with availability information based on ingredient stock."""
            return self.service.get_all_with_availability(offset, limit)
