from src.controllers.base_implementation import BaseControllerImplementation
from src.schemas.manufactured_item import (
    CreateManufacturedItemSchema,
    ResponseManufacturedItemSchema,
    ResponseManufacturedItemWithAvailabilitySchema,
)
from src.schemas.pagination import PaginatedResponseSchema
from src.services.manufactured_item import ManufacturedItemService


class ManufacturedItemController(BaseControllerImplementation):
    """Controlador para manejar los items manufacturados."""

    def __init__(self):
        super().__init__(
            create_schema=CreateManufacturedItemSchema,
            response_schema=ResponseManufacturedItemSchema,
            service=ManufacturedItemService(),
            tags=["Manufactured Item"],
        )

        @self.router.get(
            "/products/{id_key}",
            response_model=ResponseManufacturedItemWithAvailabilitySchema,
        )
        def get_public_product(
            id_key: int,
        ) -> ResponseManufacturedItemWithAvailabilitySchema:
            """Endpoint publico para un producto por ID."""
            return self.service.get_one(id_key)

        @self.router.get("/products/all", response_model=PaginatedResponseSchema)
        def get_public_products(
            offset: int = 0, limit: int = 10
        ) -> PaginatedResponseSchema:
            """Endpoint publico para productos."""
            return self.service.get_all(offset, limit)
