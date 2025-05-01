from src.schemas.base import BaseSchema


class BaseIngredientCategorySchema(BaseSchema):
    name: str
    description: str = None
    active: bool = True


class CreateIngredientCategorySchema(BaseIngredientCategorySchema):
    pass


class ResponseIngredientCategorySchema(CreateIngredientCategorySchema):
    id_key: int
