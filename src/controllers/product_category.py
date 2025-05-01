from src.controllers.base_implementation import BaseControllerImplementation
from src.schemas.product_category import (
    CreateProductCategorySchema,
    ResponseProductCategorySchema,
)
from src.services.product_category import ProductCategoryService


class ProductCategoryController(BaseControllerImplementation):
    def __init__(self):
        super().__init__(
            create_schema=CreateProductCategorySchema,
            response_schema=ResponseProductCategorySchema,
            service=ProductCategoryService(),
            tags=["Product Category"],
        )
