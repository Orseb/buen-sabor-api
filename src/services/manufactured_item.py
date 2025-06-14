from src.models.manufactured_item import ManufacturedItemModel
from src.repositories.manufactured_item import ManufacturedItemRepository
from src.repositories.manufactured_item_detail import ManufacturedItemDetailRepository
from src.schemas.manufactured_item import (
    CreateManufacturedItemSchema,
    ResponseManufacturedItemSchema,
    ResponseManufacturedItemWithAvailabilitySchema,
)
from src.schemas.pagination import PaginatedResponseSchema
from src.services.base_implementation import BaseServiceImplementation
from src.services.inventory_item import InventoryItemService
from src.utils.cloudinary import (
    delete_image_from_cloudinary,
    upload_base64_image_to_cloudinary,
)


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

        details = schema.details
        schema.details = []
        return self.repository.save_with_details(self.to_model(schema), details)

    def update(
        self, id_key: int, schema: CreateManufacturedItemSchema
    ) -> ResponseManufacturedItemSchema:
        """Update a manufactured item with its details"""
        manufactured_item = self.get_one(id_key)
        if schema.image_url and schema.image_url != manufactured_item.image_url:
            schema.image_url = upload_base64_image_to_cloudinary(
                schema.image_url, "manufactured_items"
            )

        details = schema.details
        schema.details = []
        return self.repository.update_with_details(id_key, schema, details)

    def delete(self, id_key: int) -> ResponseManufacturedItemSchema:
        """Delete a manufactured item and its image from Cloudinary."""
        manufactured_item = self.repository.find(id_key)
        if manufactured_item.image_url:
            try:
                delete_image_from_cloudinary(manufactured_item.image_url)
            except Exception as e:
                print("Failed to delete image from Cloudinary:", e)

        return self.repository.remove(id_key)

    def get_all_with_availability(
        self, offset: int = 0, limit: int = 10
    ) -> PaginatedResponseSchema:
        """Get all manufactured items with availability information."""
        # Get regular paginated results
        paginated_result = self.get_all(offset, limit)

        # Convert items to include availability
        items_with_availability = []
        for item in paginated_result.items:
            is_available = self._check_item_availability(item)
            item_dict = item.model_dump()
            item_dict["is_available"] = is_available
            items_with_availability.append(
                ResponseManufacturedItemWithAvailabilitySchema(**item_dict)
            )

        return PaginatedResponseSchema(
            total=paginated_result.total,
            offset=paginated_result.offset,
            limit=paginated_result.limit,
            items=items_with_availability,
        )

    def _check_item_availability(
        self, manufactured_item: ResponseManufacturedItemSchema
    ) -> bool:
        """Check if a manufactured item can be produced based on ingredient stock."""
        if not manufactured_item.details:
            # If no ingredients are required, it's available
            return True

        for detail in manufactured_item.details:
            inventory_item = self.inventory_item_service.get_one(
                detail.inventory_item.id_key
            )

            # Check if there's enough stock for this ingredient
            if inventory_item.current_stock < detail.quantity:
                return False

        return True

    def check_single_item_availability(self, manufactured_item_id: int) -> bool:
        """Check availability for a single manufactured item."""
        manufactured_item = self.get_one(manufactured_item_id)
        return self._check_item_availability(manufactured_item)
