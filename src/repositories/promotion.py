from typing import List

from src.models.promotion import PromotionModel
from src.models.promotion_inventory_item_detail import PromotionInventoryItemDetailModel
from src.models.promotion_manufactured_item_detail import (
    PromotionManufacturedItemDetailModel,
)
from src.repositories.base_implementation import (
    BaseRepositoryImplementation,
    RecordNotFoundError,
)
from src.schemas.promotion import CreatePromotionSchema, ResponsePromotionSchema
from src.schemas.promotion_inventory_item_detail import (
    CreatePromotionInventoryItemDetailSchema,
)
from src.schemas.promotion_manufactured_item_detail import (
    CreatePromotionManufacturedItemDetailSchema,
)


class PromotionRepository(BaseRepositoryImplementation):
    """Repositorio para manejar las promociones."""

    def __init__(self):
        super().__init__(
            model=PromotionModel,
            create_schema=CreatePromotionSchema,
            response_schema=ResponsePromotionSchema,
        )

    def save_with_details(
        self,
        promotion_model: PromotionModel,
        manufactured_item_details: List[CreatePromotionManufacturedItemDetailSchema],
        inventory_item_details: List[CreatePromotionInventoryItemDetailSchema],
    ) -> ResponsePromotionSchema:
        """Guarda una promoción junto con sus detalles de items."""
        with self.session_scope() as session:
            session.add(promotion_model)
            session.flush()

            for detail in manufactured_item_details:
                detail_dict = detail.model_dump()
                detail_dict["promotion_id"] = promotion_model.id_key
                detail_model = PromotionManufacturedItemDetailModel(**detail_dict)
                session.add(detail_model)

            for detail in inventory_item_details:
                detail_dict = detail.model_dump()
                detail_dict["promotion_id"] = promotion_model.id_key
                detail_model = PromotionInventoryItemDetailModel(**detail_dict)
                session.add(detail_model)

            session.flush()
            session.refresh(promotion_model)

            return self.schema.model_validate(promotion_model)

    def update_with_details(
        self,
        id_key: int,
        schema: CreatePromotionSchema,
        manufactured_item_details: List[CreatePromotionManufacturedItemDetailSchema],
        inventory_item_details: List[CreatePromotionInventoryItemDetailSchema],
    ) -> ResponsePromotionSchema:
        """Actualiza una promoción junto con sus detalles de items."""
        with self.session_scope() as session:
            promotion_model = session.get(self.model, id_key)
            if promotion_model is None:
                raise RecordNotFoundError(f"No record found with id {id_key}")

            for key, value in schema.model_dump(
                exclude={"manufactured_item_details", "inventory_item_details"}
            ).items():
                if hasattr(promotion_model, key) and value is not None:
                    setattr(promotion_model, key, value)

            for detail in promotion_model.manufactured_item_details:
                session.delete(detail)
            for detail in promotion_model.inventory_item_details:
                session.delete(detail)

            for detail in manufactured_item_details:
                detail_dict = detail.model_dump()
                detail_dict["promotion_id"] = promotion_model.id_key
                detail_model = PromotionManufacturedItemDetailModel(**detail_dict)
                session.add(detail_model)

            for detail in inventory_item_details:
                detail_dict = detail.model_dump()
                detail_dict["promotion_id"] = promotion_model.id_key
                detail_model = PromotionInventoryItemDetailModel(**detail_dict)
                session.add(detail_model)

            session.flush()
            session.refresh(promotion_model)

            return self.schema.model_validate(promotion_model)
