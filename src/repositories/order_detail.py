from datetime import datetime
from typing import Any, Dict, List

from sqlalchemy import desc, func

from src.models.manufactured_item import ManufacturedItemModel
from src.models.manufactured_item_category import ManufacturedItemCategoryModel
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
            filters = [
                OrderModel.status == "entregado",
                OrderDetailModel.manufactured_item_id.isnot(None),
            ]
            if start_date:
                filters.append(OrderModel.date >= start_date)
            if end_date:
                filters.append(OrderModel.date <= end_date)

            results = (
                session.query(
                    ManufacturedItemModel.id_key,
                    ManufacturedItemModel.name,
                    ManufacturedItemCategoryModel.name.label("category_name"),
                    func.sum(OrderDetailModel.quantity).label("total_quantity"),
                    func.sum(OrderDetailModel.subtotal).label("total_revenue"),
                )
                .select_from(OrderDetailModel)
                .join(OrderModel)
                .join(ManufacturedItemModel)
                .outerjoin(ManufacturedItemModel.category)
                .filter(*filters)
                .group_by(
                    ManufacturedItemModel.id_key,
                    ManufacturedItemModel.name,
                    ManufacturedItemCategoryModel.name,
                )
                .order_by(desc(func.sum(OrderDetailModel.quantity)))
                .limit(limit)
                .all()
            )

            return [
                {
                    "id": r.id_key,
                    "name": r.name,
                    "quantity": r.total_quantity,
                    "revenue": r.total_revenue,
                    "category": r.category_name or "Unknown",
                    "type": "manufactured_item",
                }
                for r in results
            ]
