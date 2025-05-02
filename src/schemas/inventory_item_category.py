from src.schemas.base import BaseSchema


class BaseInventoryItemCategorySchema(BaseSchema):
    name: str
    description: str = None
    active: bool = True


class CreateInventoryItemCategorySchema(BaseInventoryItemCategorySchema):
    pass


class ResponseInventoryItemCategorySchema(CreateInventoryItemCategorySchema):
    id_key: int
