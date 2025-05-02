from src.schemas.base import BaseSchema


class BaseManufacturedItemCategorySchema(BaseSchema):
    name: str
    description: str = None
    active: bool = True


class CreateManufacturedItemCategorySchema(BaseManufacturedItemCategorySchema):
    pass


class ResponseManufacturedItemCategorySchema(CreateManufacturedItemCategorySchema):
    id_key: int
