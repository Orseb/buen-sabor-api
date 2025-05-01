from src.controllers.base_implementation import BaseControllerImplementation
from src.schemas.ingredient_category import (
    CreateIngredientCategorySchema,
    ResponseIngredientCategorySchema,
)
from src.services.ingredient_category import IngredientCategoryService


class IngredientCategoryController(BaseControllerImplementation):
    def __init__(self):
        super().__init__(
            create_schema=CreateIngredientCategorySchema,
            response_schema=ResponseIngredientCategorySchema,
            service=IngredientCategoryService(),
            tags=["Ingredient Category"],
        )
