from datetime import datetime
from typing import Any, Dict, List

from sqlalchemy import desc, func

from src.models.inventory_item import InventoryItemModel
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
            results = (
                session.query(
                    OrderInventoryDetailModel.inventory_item_id,
                    func.sum(OrderInventoryDetailModel.quantity).label(
                        "total_quantity"
                    ),
                    func.sum(OrderInventoryDetailModel.subtotal).label("total_revenue"),
                )
                .join(OrderModel)
                .filter(
                    OrderModel.date >= start_date if start_date else True,
                    OrderModel.date <= end_date if end_date else True,
                    OrderModel.status == "entregado",
                )
                .group_by(OrderInventoryDetailModel.inventory_item_id)
                .order_by(desc("total_quantity"))
                .limit(limit)
                .all()
            )

            top_products = []
            for result in results:
                inventory_item = session.query(InventoryItemModel).get(result[0])
                if inventory_item:
                    top_products.append(
                        {
                            "id": inventory_item.id_key,
                            "name": inventory_item.name,
                            "quantity": result[1],
                            "revenue": result[2],
                            "category": (
                                inventory_item.category.name
                                if inventory_item.category
                                else "Unknown"
                            ),
                            "type": "inventory_item",
                        }
                    )

            return top_products
