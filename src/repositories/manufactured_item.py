from src.models.manufactured_item import ManufacturedItemModel
from src.models.manufactured_item_detail import ManufacturedItemDetailModel
from src.repositories.base_implementation import (
    BaseRepositoryImplementation,
    RecordNotFoundError,
)
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

            for detail in details:
                detail_dict = detail.model_dump()
                detail_dict["manufactured_item_id"] = manufactured_item_model.id_key
                detail_model = ManufacturedItemDetailModel(**detail_dict)
                session.add(detail_model)

            session.flush()
            session.refresh(manufactured_item_model)

            return self.schema.model_validate(manufactured_item_model)

    def update_with_details(
        self, id_key, schema, details
    ) -> ResponseManufacturedItemSchema:
        with self.session_scope() as session:
            manufactured_item_model = session.get(self.model, id_key)
            if manufactured_item_model is None:
                raise RecordNotFoundError(f"No record found with id {id_key}")

            for key, value in schema.model_dump().items():
                if hasattr(manufactured_item_model, key) and value is not None:
                    setattr(manufactured_item_model, key, value)

            for detail in details:
                detail_dict = detail.model_dump()
                detail_dict["manufactured_item_id"] = manufactured_item_model.id_key
                detail_model = ManufacturedItemDetailModel(**detail_dict)
                session.add(detail_model)

            session.flush()
            session.refresh(manufactured_item_model)

            return self.schema.model_validate(manufactured_item_model)
