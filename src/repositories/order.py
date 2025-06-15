from datetime import datetime
from typing import Any, Dict, List

from sqlalchemy import desc, func

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
        with self.session_scope() as session:
            if status:
                return (
                    session.query(self.model)
                    .filter(self.model.user_id == user_id, self.model.status == status)
                    .count()
                )

            return (
                session.query(self.model).filter(self.model.user_id == user_id).count()
            )

    def find_by_user(
        self, user_id: int, status: OrderStatus | None, offset: int, limit: int
    ) -> List[ResponseOrderSchema]:
        """Obtiene los pedidos de un usuario, opcionalmente filtrando por estado."""
        with self.session_scope() as session:
            if status:
                models = (
                    session.query(self.model)
                    .filter(self.model.user_id == user_id, self.model.status == status)
                    .order_by(desc(self.model.date))
                    .offset(offset)
                    .limit(limit)
                    .all()
                )
            else:
                models = (
                    session.query(self.model)
                    .filter(self.model.user_id == user_id)
                    .order_by(desc(self.model.date))
                    .offset(offset)
                    .limit(limit)
                    .all()
                )
            return [self.schema.model_validate(model) for model in models]

    def get_top_customers(
        self, start_date: datetime, end_date: datetime, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Obtiene los clientes con más pedidos en un rango de fechas."""
        with self.session_scope() as session:
            results = (
                session.query(
                    OrderModel.user_id,
                    func.count(OrderModel.id_key).label("order_count"),
                    func.sum(OrderModel.final_total).label("total_amount"),
                )
                .filter(
                    OrderModel.date >= start_date if start_date else True,
                    OrderModel.date <= end_date if end_date else True,
                    OrderModel.status == "entregado",
                )
                .group_by(OrderModel.user_id)
                .order_by(desc("order_count"))
                .limit(limit)
                .all()
            )

            top_customers = []
            for result in results:
                user = session.query(UserModel).get(result[0])
                if user:
                    top_customers.append(
                        {
                            "id": user.id_key,
                            "name": user.full_name,
                            "email": user.email,
                            "order_count": result[1],
                            "total_amount": result[2],
                        }
                    )

            return top_customers
