from src.models.order_detail import OrderDetailModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.order_detail import (
    CreateOrderDetailSchema,
    ResponseOrderDetailSchema,
)


class OrderDetailRepository(BaseRepositoryImplementation):
    def __init__(self):
        super().__init__(
            model=OrderDetailModel,
            create_schema=CreateOrderDetailSchema,
            response_schema=ResponseOrderDetailSchema,
        )
