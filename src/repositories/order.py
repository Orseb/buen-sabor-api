from datetime import datetime
from typing import Any, Dict, List

from sqlalchemy import String, desc, func, select

from src.models.order import OrderModel, OrderStatus
from src.models.order_detail import OrderDetailModel
from src.models.order_inventory_detail import OrderInventoryDetailModel
from src.models.user import UserModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.repositories.inventory_item import InventoryItemRepository
from src.repositories.manufactured_item import ManufacturedItemRepository
from src.schemas.order import CreateOrderSchema, ResponseOrderSchema
from src.schemas.order_detail import CreateOrderDetailSchema
from src.schemas.order_inventory_detail import CreateOrderInventoryDetailSchema


class OrderRepository(BaseRepositoryImplementation):
    """Repositorio para manejo de pedidos."""

    def __init__(self):
        super().__init__(
            model=OrderModel,
            create_schema=CreateOrderSchema,
            response_schema=ResponseOrderSchema,
        )
        self.manufactured_item_repository = ManufacturedItemRepository()
        self.inventory_item_repository = InventoryItemRepository()

    def save_with_details(
        self,
        order_model: OrderModel,
        details: List[CreateOrderDetailSchema],
        inventory_details: List[CreateOrderInventoryDetailSchema],
    ) -> ResponseOrderSchema:
        """Guarda un pedido con sus detalles y detalles de inventario."""
        with self.session_scope() as session:
            session.add(order_model)
            session.flush()

            for detail in details:
                detail_dict = detail.model_dump()
                detail_dict["order_id"] = order_model.id_key
                detail_model = OrderDetailModel(**detail_dict)
                session.add(detail_model)

            for detail in inventory_details:
                detail_dict = detail.model_dump()
                detail_dict["order_id"] = order_model.id_key
                inventory_detail_model = OrderInventoryDetailModel(**detail_dict)
                session.add(inventory_detail_model)

            session.flush()
            session.refresh(order_model)

            return self.schema.model_validate(order_model)

    def count_all_by_user(self, user_id: int, status: OrderStatus | None) -> int:
        """Cuenta todos los pedidos de un usuario, opcionalmente filtrando por estado."""
        stmt = select(func.count()).where(self.model.user_id == user_id)
        if status:
            stmt = stmt.where(self.model.status == status)

        with self.session_scope() as session:
            return session.scalar(stmt)

    def find_by_user(
        self, user_id: int, status: OrderStatus | None, offset: int, limit: int
    ) -> List[ResponseOrderSchema]:
        """Obtiene los pedidos de un usuario, opcionalmente filtrando por estado."""
        stmt = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .order_by(desc(self.model.date))
            .offset(offset)
            .limit(limit)
        )

        if status:
            stmt = stmt.where(self.model.status == status)

        with self.session_scope() as session:
            result = session.execute(stmt)
            return [self.schema.model_validate(row) for row in result.scalars()]

    def get_top_customers(
        self, start_date: datetime, end_date: datetime, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Obtiene los clientes con más pedidos en un rango de fechas."""
        with self.session_scope() as session:
            filters = [OrderModel.status == "entregado"]
            if start_date:
                filters.append(OrderModel.date >= start_date)
            if end_date:
                filters.append(OrderModel.date <= end_date)

            results = (
                session.query(
                    UserModel.id_key,
                    UserModel.full_name,
                    UserModel.email,
                    func.count(OrderModel.id_key).label("order_count"),
                    func.sum(OrderModel.final_total).label("total_amount"),
                )
                .join(OrderModel.user)
                .filter(*filters)
                .group_by(UserModel.id_key, UserModel.full_name, UserModel.email)
                .order_by(desc(func.count(OrderModel.id_key)))
                .limit(limit)
                .all()
            )

            return [
                {
                    "id": r.id_key,
                    "name": r.full_name,
                    "email": r.email,
                    "order_count": r.order_count,
                    "total_amount": r.total_amount,
                }
                for r in results
            ]

    def search_orders_by_id(
        self, search_term: str, offset: int, limit: int
    ) -> List[ResponseOrderSchema]:
        """Busca órdenes activas por ID."""
        with self.session_scope() as session:
            stmt = (
                select(self.model)
                .where(
                    func.cast(self.model.id_key, String).ilike(f"%{search_term}%"),
                    self.model.active.is_(True),
                )
                .order_by(desc(self.model.date))
                .offset(offset)
                .limit(limit)
            )

            result = session.execute(stmt)
            return [self.schema.model_validate(row) for row in result.scalars()]

    def count_search_orders_by_id(self, search_term: str) -> int:
        """Cuenta órdenes activas que coinciden con el término de búsqueda por ID."""
        with self.session_scope() as session:
            stmt = select(func.count()).where(
                func.cast(self.model.id_key, String).ilike(f"%{search_term}%"),
                self.model.active.is_(True),
            )
            return session.scalar(stmt)
