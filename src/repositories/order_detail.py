from datetime import datetime
from typing import Any, Dict, List

from sqlalchemy import desc, func

from src.models.manufactured_item import ManufacturedItemModel
from src.models.order import OrderModel
from src.models.order_detail import OrderDetailModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.order_detail import (
    CreateOrderDetailSchema,
    ResponseOrderDetailSchema,
)


class OrderDetailRepository(BaseRepositoryImplementation):
    """Repositorio para manejar los detalles de los pedidos."""

    def __init__(self):
        super().__init__(
            model=OrderDetailModel,
            create_schema=CreateOrderDetailSchema,
            response_schema=ResponseOrderDetailSchema,
        )

    def get_top_manufactured_products(
        self, start_date: datetime, end_date: datetime, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Obtiene los productos manufacturados más vendidos en un rango de fechas."""
        with self.session_scope() as session:
            results = (
                session.query(
                    OrderDetailModel.manufactured_item_id,
                    func.sum(OrderDetailModel.quantity).label("total_quantity"),
                    func.sum(OrderDetailModel.subtotal).label("total_revenue"),
                )
                .join(OrderModel)
                .filter(
                    OrderModel.date >= start_date if start_date else True,
                    OrderModel.date <= end_date if end_date else True,
                    OrderModel.status == "entregado",
                )
                .group_by(OrderDetailModel.manufactured_item_id)
                .order_by(desc("total_quantity"))
                .limit(limit)
                .all()
            )

            top_products = []
            for result in results:
                manufactured_item = session.query(ManufacturedItemModel).get(result[0])
                if manufactured_item:
                    top_products.append(
                        {
                            "id": manufactured_item.id_key,
                            "name": manufactured_item.name,
                            "quantity": result[1],
                            "revenue": result[2],
                            "category": (
                                manufactured_item.category.name
                                if manufactured_item.category
                                else "Unknown"
                            ),
                            "type": "manufactured_item",
                        }
                    )

            return top_products
