from src.schemas.base import BaseSchema


class BaseProductCategorySchema(BaseSchema):
    name: str
    description: str = None
    active: bool = True


class CreateProductCategorySchema(BaseProductCategorySchema):
    pass


class ResponseProductCategorySchema(CreateProductCategorySchema):
    id_key: int
