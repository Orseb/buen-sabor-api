from src.models.manufactured_item import ManufacturedItemModel
from src.models.manufactured_item_detail import ManufacturedItemDetailModel
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
        details = schema.details
        schema.details = []

        if schema.image_url:
            schema.image_url = upload_base64_image_to_cloudinary(
                schema.image_url, "manufactured_items"
            )

        manufactured_item = super().save(schema)

        for detail in details:
            detail_dict = detail.model_dump()
            detail_dict["manufactured_item_id"] = manufactured_item.id_key
            detail_model = ManufacturedItemDetailModel(**detail_dict)
            self.manufactured_item_detail_repository.save(detail_model)

        return self.get_one(manufactured_item.id_key)

    def update(
        self, id_key: int, schema: CreateManufacturedItemSchema
    ) -> ResponseManufacturedItemSchema:
        """Update a manufactured item with its details"""
        details = schema.details
        schema.details = []
        manufactured_item = super().update(id_key, schema)

        with self.repository.session_scope() as session:
            details_to_delete = (
                session.query(self.manufactured_item_detail_repository.model)
                .filter(
                    self.manufactured_item_detail_repository.model.manufactured_item_id
                    == id_key
                )
                .all()
            )
            for detail in details_to_delete:
                session.delete(detail)

        for detail in details:
            detail_dict = detail.model_dump()
            detail_dict["manufactured_item_id"] = manufactured_item.id_key
            detail_model = ManufacturedItemDetailModel(**detail_dict)
            self.manufactured_item_detail_repository.save(detail_model)

        return self.get_one(manufactured_item.id_key)

    def check_stock_availability(
        self, manufactured_item_id: int, quantity: int = 1
    ) -> bool:
        """Check if there is enough stock to prepare a manufactured item"""
        manufactured_item = self.get_one(manufactured_item_id)

        for detail in manufactured_item.details:
            inventory_item = self.inventory_item_service.get_one(
                detail.inventory_item.id_key
            )
            if inventory_item.current_stock < detail.quantity * quantity:
                return False

        return True

    def get_max_quantity_available(self, manufactured_item_id: int) -> int:
        """Get the maximum quantity of a manufactured item that can be prepared"""
        manufactured_item = self.get_one(manufactured_item_id)
        max_quantity = float("inf")

        for detail in manufactured_item.details:
            inventory_item = self.inventory_item_service.get_one(
                detail.inventory_item.id_key
            )
            if detail.quantity > 0:
                available = inventory_item.current_stock // detail.quantity
                max_quantity = min(max_quantity, available)

        return max_quantity if max_quantity != float("inf") else 0

    def update_image(
        self, id_key: int, base64_image: str
    ) -> ResponseManufacturedItemSchema:
        image_url = upload_base64_image_to_cloudinary(
            base64_image, "manufactured_items"
        )
        return self.repository.update(id_key, {"image_url": image_url})
