from src.models.inventory_item import InventoryItemModel
from src.repositories.inventory_item import InventoryItemRepository
from src.schemas.inventory_item import (
    CreateInventoryItemSchema,
    ResponseInventoryItemSchema,
)
from src.services.base_implementation import BaseServiceImplementation
from src.utils.cloudinary import upload_base64_image_to_cloudinary


class InventoryItemService(BaseServiceImplementation):

    def __init__(self):
        super().__init__(
            repository=InventoryItemRepository(),
            model=InventoryItemModel,
            create_schema=CreateInventoryItemSchema,
            response_schema=ResponseInventoryItemSchema,
        )

    def save(self, schema: CreateInventoryItemSchema) -> ResponseInventoryItemSchema:
        """Save an inventory item"""

        if schema.image_url:
            schema.image_url = upload_base64_image_to_cloudinary(
                schema.image_url, "inventory_items"
            )

        return super().save(schema)

    def update_image(
        self, id_key: int, base64_image: str
    ) -> ResponseInventoryItemSchema:
        image_url = upload_base64_image_to_cloudinary(base64_image, "inventory_items")
        return self.repository.update(id_key, {"image_url": image_url})
