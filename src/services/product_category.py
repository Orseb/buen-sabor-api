from src.models.product_category import ProductCategoryModel
from src.repositories.product_category import ProductCategoryRepository
from src.schemas.product_category import (
    CreateProductCategorySchema,
    ResponseProductCategorySchema,
)
from src.services.base_implementation import BaseServiceImplementation


class ProductCategoryService(BaseServiceImplementation):

    def __init__(self):
        super().__init__(
            repository=ProductCategoryRepository(),
            model=ProductCategoryModel,
            create_schema=CreateProductCategorySchema,
            response_schema=ResponseProductCategorySchema,
        )
