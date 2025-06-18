from datetime import datetime
from typing import Any, Dict, List

from sqlalchemy import desc, func

from src.models.inventory_item import InventoryItemModel
from src.models.inventory_item_category import InventoryItemCategoryModel
from src.models.order import OrderModel
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

    def get_top_inventory_products(
        self, start_date: datetime, end_date: datetime, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Obtiene los productos de inventario más vendidos en un rango de fechas."""
        with self.session_scope() as session:
            filters = [
                OrderModel.status == "entregado",
                OrderInventoryDetailModel.inventory_item_id.isnot(None),
            ]
            if start_date:
                filters.append(OrderModel.date >= start_date)
            if end_date:
                filters.append(OrderModel.date <= end_date)

            results = (
                session.query(
                    InventoryItemModel.id_key,
                    InventoryItemModel.name,
                    InventoryItemCategoryModel.name.label("category_name"),
                    func.sum(OrderInventoryDetailModel.quantity).label(
                        "total_quantity"
                    ),
                    func.sum(OrderInventoryDetailModel.subtotal).label("total_revenue"),
                )
                .select_from(OrderInventoryDetailModel)
                .join(OrderModel)
                .join(InventoryItemModel)
                .outerjoin(InventoryItemModel.category)
                .filter(*filters)
                .group_by(
                    InventoryItemModel.id_key,
                    InventoryItemModel.name,
                    InventoryItemCategoryModel.name,
                )
                .order_by(desc(func.sum(OrderInventoryDetailModel.quantity)))
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
                    "type": "inventory_item",
                }
                for r in results
            ]
