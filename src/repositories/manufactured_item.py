from src.models.manufactured_item import ManufacturedItemModel
from src.models.manufactured_item_detail import ManufacturedItemDetailModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.manufactured_item import (
    CreateManufacturedItemSchema,
    ResponseManufacturedItemSchema,
)


class ManufacturedItemRepository(BaseRepositoryImplementation):
    def __init__(self):
        super().__init__(
            model=ManufacturedItemModel,
            create_schema=CreateManufacturedItemSchema,
            response_schema=ResponseManufacturedItemSchema,
        )

    def save_with_details(
        self, manufactured_item_model, details
    ) -> ResponseManufacturedItemSchema:
        with self.session_scope() as session:
            session.add(manufactured_item_model)
            session.flush()
            manufactured_item_id = manufactured_item_model.id_key

            for detail in details:
                detail_dict = detail.model_dump()
                detail_dict["manufactured_item_id"] = manufactured_item_id
                detail_model = ManufacturedItemDetailModel(**detail_dict)
                session.add(detail_model)

            session.flush()
            session.refresh(manufactured_item_model)

            return self.schema.model_validate(manufactured_item_model)
