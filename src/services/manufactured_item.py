from src.models.manufactured_item import ManufacturedItemModel
from src.repositories.inventory_item import InventoryItemRepository
from src.repositories.manufactured_item import ManufacturedItemRepository
from src.repositories.manufactured_item_detail import ManufacturedItemDetailRepository
from src.schemas.manufactured_item import (
    CreateManufacturedItemSchema,
    ResponseManufacturedItemSchema,
    ResponseManufacturedItemWithAvailabilitySchema,
)
from src.schemas.pagination import PaginatedResponseSchema
from src.services.base_implementation import BaseServiceImplementation
from src.utils.cloudinary import (
    delete_image_from_cloudinary,
    upload_base64_image_to_cloudinary,
)


class ManufacturedItemService(BaseServiceImplementation):
    """Servicio para manejar la lógica de negocio relacionada con los items manufacturados."""

    def __init__(self):
        super().__init__(
            repository=ManufacturedItemRepository(),
            model=ManufacturedItemModel,
            create_schema=CreateManufacturedItemSchema,
            response_schema=ResponseManufacturedItemSchema,
        )
        self.manufactured_item_detail_repository = ManufacturedItemDetailRepository()
        self.inventory_item_repository = InventoryItemRepository()

    def get_one(self, id_key: int) -> ResponseManufacturedItemSchema:
        """Obtiene un item manufacturado por su ID."""
        manufactured_item = super().get_one(id_key)
        is_available = self._check_item_availability(manufactured_item)
        item_dict = manufactured_item.model_dump()
        item_dict["is_available"] = is_available
        return ResponseManufacturedItemWithAvailabilitySchema(**item_dict)

    def get_all(self, offset: int = 0, limit: int = 10) -> PaginatedResponseSchema:
        """Obtiene todos los items manufacturados con su disponibilidad."""
        paginated_result = super().get_all(offset, limit)

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

    def save(
        self, schema: CreateManufacturedItemSchema
    ) -> ResponseManufacturedItemSchema:
        """Guarda un nuevo item manufacturado en la base de datos."""
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
        """Actualiza un item manufacturado existente en la base de datos."""
        manufactured_item = self.repository.find(id_key)
        if schema.image_url and schema.image_url != manufactured_item.image_url:
            schema.image_url = upload_base64_image_to_cloudinary(
                schema.image_url, "manufactured_items"
            )
        details = schema.details
        schema.details = []

        return self.repository.update_with_details(id_key, schema, details)

    def delete(self, id_key: int) -> ResponseManufacturedItemSchema:
        """Elimina un item manufacturado de la base de datos."""
        manufactured_item = self.repository.find(id_key)
        if manufactured_item.image_url:
            delete_image_from_cloudinary(manufactured_item.image_url)

        return self.repository.remove(id_key)

    def _check_item_availability(
        self, manufactured_item: ResponseManufacturedItemSchema
    ) -> bool:
        """Verifica si un item manufacturado tiene suficiente stock para elaborarse."""
        for detail in manufactured_item.details:
            inventory_item = self.inventory_item_repository.find(
                detail.inventory_item.id_key
            )

            if inventory_item.current_stock < detail.quantity:
                return False

        return True
