from src.controllers.base_implementation import BaseControllerImplementation
from src.schemas.promotion import CreatePromotionSchema, ResponsePromotionSchema
from src.services.promotion import PromotionService


class PromotionController(BaseControllerImplementation):
    """Controlador para manejar las promociones."""

    def __init__(self):
        super().__init__(
            create_schema=CreatePromotionSchema,
            response_schema=ResponsePromotionSchema,
            service=PromotionService(),
            tags=["Promotion"],
        )
