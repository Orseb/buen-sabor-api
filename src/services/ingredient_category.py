from src.models.ingredient_category import IngredientCategoryModel
from src.repositories.ingredient_category import IngredientCategoryRepository
from src.schemas.ingredient_category import (
    CreateIngredientCategorySchema,
    ResponseIngredientCategorySchema,
)
from src.services.base_implementation import BaseServiceImplementation


class IngredientCategoryService(BaseServiceImplementation):

    def __init__(self):
        super().__init__(
            repository=IngredientCategoryRepository(),
            model=IngredientCategoryModel,
            create_schema=CreateIngredientCategorySchema,
            response_schema=ResponseIngredientCategorySchema,
        )
