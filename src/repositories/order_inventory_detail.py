from src.models.order_inventory_detail import OrderInventoryDetailModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.order_inventory_detail import (
    CreateOrderInventoryDetailSchema,
    ResponseOrderInventoryDetailSchema,
)


class OrderInventoryDetailRepository(BaseRepositoryImplementation):
    """Repositorio para manejar los detalles de inventario de pedidos."""

    def __init__(self):
        super().__init__(
            model=OrderInventoryDetailModel,
            create_schema=CreateOrderInventoryDetailSchema,
            response_schema=ResponseOrderInventoryDetailSchema,
        )
