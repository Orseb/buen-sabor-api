from src.models.inventory_item import InventoryItemModel
from src.repositories.inventory_item import InventoryItemRepository
from src.schemas.inventory_item import (
    CreateInventoryItemSchema,
    ResponseInventoryItemSchema,
)
from src.services.base_implementation import BaseServiceImplementation
from src.utils.cloudinary import upload_base64_image_to_cloudinary


class InventoryItemService(BaseServiceImplementation):
    """Servicio para manejar la lógica de negocio relacionada con los artículos de inventario."""

    def __init__(self):
        super().__init__(
            repository=InventoryItemRepository(),
            model=InventoryItemModel,
            create_schema=CreateInventoryItemSchema,
            response_schema=ResponseInventoryItemSchema,
        )

    def save(self, schema: CreateInventoryItemSchema) -> ResponseInventoryItemSchema:
        """Guarda un nuevo artículo de inventario, subiendo la imagen si es necesario."""
        if schema.image_url:
            schema.image_url = upload_base64_image_to_cloudinary(
                schema.image_url, "inventory_items"
            )

        return super().save(schema)

    def update(
        self, id_key: int, schema: CreateInventoryItemSchema
    ) -> ResponseInventoryItemSchema:
        """Actualiza un artículo de inventario existente, subiendo la imagen si es necesario."""
        inventory_item = self.repository.find(id_key)
        if schema.image_url and schema.image_url != inventory_item.image_url:
            schema.image_url = upload_base64_image_to_cloudinary(
                schema.image_url, "inventory_items"
            )

        return super().update(id_key, schema)
