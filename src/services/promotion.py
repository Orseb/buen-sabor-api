from src.models.promotion import PromotionModel
from src.repositories.promotion import PromotionRepository
from src.schemas.pagination import PaginatedResponseSchema
from src.schemas.promotion import (
    CreatePromotionSchema,
    ResponsePromotionSchema,
    ResponsePromotionWithAvailabilitySchema,
)
from src.services.base_implementation import BaseServiceImplementation
from src.services.manufactured_item import ManufacturedItemService


class PromotionService(BaseServiceImplementation):
    """Servicio para manejar la lógica de negocio relacionada con las promociones."""

    def __init__(self):
        super().__init__(
            repository=PromotionRepository(),
            model=PromotionModel,
            create_schema=CreatePromotionSchema,
            response_schema=ResponsePromotionSchema,
        )
        self.manufactured_item_service = ManufacturedItemService()

    def get_all(self, offset: int = 0, limit: int = 10) -> PaginatedResponseSchema:
        """Obtiene todas las promociones con su disponibilidad."""
        paginated_result = super().get_all(offset, limit)

        promotions_with_availability = []
        for promotion in paginated_result.items:
            is_available = self.check_promotion_availability(promotion)
            promotion_dict = promotion.model_dump()
            promotion_dict["is_available"] = is_available
            promotions_with_availability.append(
                ResponsePromotionWithAvailabilitySchema(**promotion_dict)
            )

        return PaginatedResponseSchema(
            total=paginated_result.total,
            offset=paginated_result.offset,
            limit=paginated_result.limit,
            items=promotions_with_availability,
        )

    def save(self, schema: CreatePromotionSchema) -> ResponsePromotionSchema:
        """Guarda una nueva promoción con sus detalles de items."""
        manufactured_item_details = schema.manufactured_item_details
        inventory_item_details = schema.inventory_item_details

        self._validate_non_ingredient_items(inventory_item_details)

        schema_dict = schema.model_dump()
        schema_dict.pop("manufactured_item_details", None)
        schema_dict.pop("inventory_item_details", None)

        promotion_model = PromotionModel(**schema_dict)

        return self.repository.save_with_details(
            promotion_model, manufactured_item_details, inventory_item_details
        )

    def update(
        self, id_key: int, schema: CreatePromotionSchema
    ) -> ResponsePromotionSchema:
        """Actualiza una promoción existente con sus detalles de items."""
        manufactured_item_details = schema.manufactured_item_details
        inventory_item_details = schema.inventory_item_details

        self._validate_non_ingredient_items(inventory_item_details)

        return self.repository.update_with_details(
            id_key, schema, manufactured_item_details, inventory_item_details
        )

    @staticmethod
    def check_promotion_availability(promotion: ResponsePromotionSchema) -> bool:
        """Verifica si una promoción tiene disponibilidad."""
        for manufactured_detail in promotion.manufactured_item_details:
            for detail in manufactured_detail.manufactured_item.details:
                if detail.inventory_item.current_stock < (
                    detail.quantity * manufactured_detail.quantity
                ):
                    return False

        for inventory_detail in promotion.inventory_item_details:
            if (
                inventory_detail.inventory_item.current_stock
                < inventory_detail.quantity
            ):
                return False
        return True

    def _validate_non_ingredient_items(self, inventory_item_details: list) -> None:
        """Valida que los items de inventario no sean ingredientes."""
        for inventory_item_detail in inventory_item_details:
            inventory_item = self.repository.find(
                inventory_item_detail.inventory_item_id
            )
            if inventory_item.is_ingredient:
                raise ValueError(
                    "No se pueden agregar ingredientes como items de inventario en una promoción."
                )
