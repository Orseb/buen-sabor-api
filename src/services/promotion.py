from src.models.promotion import PromotionModel
from src.repositories.promotion import PromotionRepository
from src.schemas.promotion import CreatePromotionSchema, ResponsePromotionSchema
from src.services.base_implementation import BaseServiceImplementation


class PromotionService(BaseServiceImplementation):
    """Servicio para manejar la lógica de negocio relacionada con las promociones."""

    def __init__(self):
        super().__init__(
            repository=PromotionRepository(),
            model=PromotionModel,
            create_schema=CreatePromotionSchema,
            response_schema=ResponsePromotionSchema,
        )

    def save(self, schema: CreatePromotionSchema) -> ResponsePromotionSchema:
        """Guarda una nueva promoción con sus detalles de items."""
        manufactured_item_details = schema.manufactured_item_details
        inventory_item_details = schema.inventory_item_details

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

        return self.repository.update_with_details(
            id_key, schema, manufactured_item_details, inventory_item_details
        )
