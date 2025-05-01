from src.models.ingredient_category import IngredientCategoryModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.ingredient_category import (
    CreateIngredientCategorySchema,
    ResponseIngredientCategorySchema,
)


class IngredientCategoryRepository(BaseRepositoryImplementation):
    def __init__(self):
        super().__init__(
            model=IngredientCategoryModel,
            create_schema=CreateIngredientCategorySchema,
            response_schema=ResponseIngredientCategorySchema,
        )
