from datetime import datetime
from typing import Dict, List, Tuple

from sqlalchemy import func

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
            purchase_costs_results = (
                session.query(
                    func.sum(InventoryPurchaseModel.total_cost).label("purchase_costs")
                )
                .filter(
                    (
                        InventoryPurchaseModel.purchase_date >= start_date
                        if start_date
                        else True
                    ),
                    (
                        InventoryPurchaseModel.purchase_date <= end_date
                        if end_date
                        else True
                    ),
                )
                .first()
            )

            purchase_count_results = (
                session.query(
                    func.count(InventoryPurchaseModel.id_key).label("purchase_count")
                )
                .filter(
                    (
                        InventoryPurchaseModel.purchase_date >= start_date
                        if start_date
                        else True
                    ),
                    (
                        InventoryPurchaseModel.purchase_date <= end_date
                        if end_date
                        else True
                    ),
                )
                .first()
            )

            return {
                "purchase_costs": purchase_costs_results.purchase_costs or 0,
                "purchase_count": purchase_count_results.purchase_count or 0,
            }

    def get_purchases_report_data(
        self, start_date: datetime, end_date: datetime
    ) -> List[Tuple[datetime, int, float, str]]:
        """Obtiene los detalles de las compras de inventario en un rango de fechas para Excel."""
        with self.session_scope() as session:
            return (
                session.query(
                    InventoryPurchaseModel.purchase_date,
                    InventoryPurchaseModel.quantity,
                    InventoryPurchaseModel.total_cost,
                    InventoryItemModel.name,
                )
                .join(InventoryItemModel)
                .filter(
                    (
                        InventoryPurchaseModel.purchase_date >= start_date
                        if start_date
                        else True
                    ),
                    (
                        InventoryPurchaseModel.purchase_date <= end_date
                        if end_date
                        else True
                    ),
                )
                .all()
            )
