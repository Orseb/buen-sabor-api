from src.models.manufactured_item import ManufacturedItemModel
from src.repositories.manufactured_item import ManufacturedItemRepository
from src.repositories.manufactured_item_detail import ManufacturedItemDetailRepository
from src.schemas.manufactured_item import (
    CreateManufacturedItemSchema,
    ResponseManufacturedItemSchema,
)
from src.services.base_implementation import BaseServiceImplementation
from src.services.inventory_item import InventoryItemService
from src.utils.cloudinary import upload_base64_image_to_cloudinary


class ManufacturedItemService(BaseServiceImplementation):
    def __init__(self):
        super().__init__(
            repository=ManufacturedItemRepository(),
            model=ManufacturedItemModel,
            create_schema=CreateManufacturedItemSchema,
            response_schema=ResponseManufacturedItemSchema,
        )
        self.manufactured_item_detail_repository = ManufacturedItemDetailRepository()
        self.inventory_item_service = InventoryItemService()

    def save(
        self, schema: CreateManufacturedItemSchema
    ) -> ResponseManufacturedItemSchema:
        """Save a manufactured item with its details"""
        if schema.image_url:
            schema.image_url = upload_base64_image_to_cloudinary(
                schema.image_url, "manufactured_items"
            )

        try:
            details = schema.details
            schema.details = []
            manufactured_item_model = self.to_model(schema)
            return self.repository.save_with_details(manufactured_item_model, details)
        except Exception as e:
            raise RuntimeError(f"Failed to save manufactured item: {e}")

    def update(
        self, id_key: int, schema: CreateManufacturedItemSchema
    ) -> ResponseManufacturedItemSchema:
        """Update a manufactured item with its details"""
        if schema.image_url:
            schema.image_url = upload_base64_image_to_cloudinary(
                schema.image_url, "manufactured_items"
            )

        try:
            details = schema.details
            schema.details = []
            return self.repository.update_with_details(id_key, schema, details)
        except Exception as e:
            raise RuntimeError(f"Failed to update manufactured item: {e}")
