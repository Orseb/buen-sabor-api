from datetime import datetime
from typing import Dict, List, Tuple

from sqlalchemy import and_, func, select
from sqlalchemy.orm import aliased

from src.models.inventory_item import InventoryItemModel
from src.models.inventory_purchase import InventoryPurchaseModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.inventory_purchase import (
    CreateInventoryPurchaseSchema,
    ResponseInventoryPurchaseSchema,
)


class InventoryPurchaseRepository(BaseRepositoryImplementation):
    """Repositorio para manejar las compras de inventario."""

    def __init__(self):
        super().__init__(
            model=InventoryPurchaseModel,
            create_schema=CreateInventoryPurchaseSchema,
            response_schema=ResponseInventoryPurchaseSchema,
        )

    def get_purchase_costs(
        self, start_date: datetime, end_date: datetime
    ) -> Dict[str, float]:
        """Obtiene los costos de compra en un rango de fechas."""
        with self.session_scope() as session:
            stmt = select(
                func.coalesce(func.sum(InventoryPurchaseModel.total_cost), 0).label(
                    "purchase_costs"
                ),
                func.count(InventoryPurchaseModel.id_key).label("purchase_count"),
            ).where(self._build_date_filter(start_date, end_date))

            result = session.execute(stmt).first()
            return {
                "purchase_costs": result.purchase_costs,
                "purchase_count": result.purchase_count,
            }

    def get_purchases_report_data(
        self, start_date: datetime, end_date: datetime
    ) -> List[Tuple[datetime, int, float, str]]:
        """Obtiene los detalles de las compras de inventario en un rango de fechas para Excel."""
        with self.session_scope() as session:
            Purchase = aliased(InventoryPurchaseModel)
            Item = aliased(InventoryItemModel)

            stmt = (
                select(
                    Purchase.purchase_date,
                    Purchase.quantity,
                    Purchase.total_cost,
                    Item.name,
                )
                .distinct()
                .select_from(Purchase)
                .join(Item, Purchase.inventory_item_id == Item.id_key)
                .where(self._build_date_filter(start_date, end_date))
            )

            result = session.execute(stmt)
            return result.all()

    def _build_date_filter(self, start_date: datetime, end_date: datetime):
        """Construye un filtro de fecha para las compras de inventario."""
        conditions = []
        if start_date:
            conditions.append(InventoryPurchaseModel.purchase_date >= start_date)
        if end_date:
            conditions.append(InventoryPurchaseModel.purchase_date <= end_date)

        return and_(*conditions) if conditions else True
