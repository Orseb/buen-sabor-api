from src.models.product_category import ProductCategoryModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.product_category import (
    CreateProductCategorySchema,
    ResponseProductCategorySchema,
)


class ProductCategoryRepository(BaseRepositoryImplementation):
    def __init__(self):
        super().__init__(
            model=ProductCategoryModel,
            create_schema=CreateProductCategorySchema,
            response_schema=ResponseProductCategorySchema,
        )
