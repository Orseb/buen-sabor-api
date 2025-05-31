from datetime import datetime
from typing import List

from sqlalchemy import desc

from src.models.invoice import InvoiceModel, InvoiceType
from src.models.order import OrderModel, OrderStatus
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.order import CreateOrderSchema, ResponseOrderSchema


class OrderRepository(BaseRepositoryImplementation):
    def __init__(self):
        super().__init__(
            model=OrderModel,
            create_schema=CreateOrderSchema,
            response_schema=ResponseOrderSchema,
        )

    def count_all_by_status(self, status: OrderStatus) -> int:
        with self.session_scope() as session:
            count = (
                session.query(self.model).filter(self.model.status == status).count()
            )
            return count

    def count_all_by_user(self, user_id: int) -> int:
        with self.session_scope() as session:
            count = (
                session.query(self.model).filter(self.model.user_id == user_id).count()
            )
            return count

    def find_by_status(
        self, status: OrderStatus, offset: int, limit: int
    ) -> List[ResponseOrderSchema]:
        with self.session_scope() as session:
            models = (
                session.query(self.model)
                .filter(self.model.status == status)
                .order_by(desc(self.model.date))
                .offset(offset)
                .limit(limit)
                .all()
            )
            return [self.schema.model_validate(model) for model in models]

    def find_by_user(
        self, user_id: int, offset: int, limit: int
    ) -> List[ResponseOrderSchema]:
        with self.session_scope() as session:
            models = (
                session.query(self.model)
                .filter(self.model.user_id == user_id)
                .order_by(desc(self.model.date))
                .offset(offset)
                .limit(limit)
                .all()
            )
            return [self.schema.model_validate(model) for model in models]

    def get_orders_by_customer(
        self,
        user_id: int,
        start_date: datetime,
        end_date: datetime,
        offset: int = 0,
        limit: int = 10,
    ) -> List[dict]:
        """Get all orders for a customer in a date range."""
        with self.session_scope() as session:
            orders = (
                session.query(OrderModel)
                .filter(
                    OrderModel.user_id == user_id,
                    OrderModel.date >= start_date,
                    OrderModel.date <= end_date,
                )
                .offset(offset)
                .limit(limit)
                .order_by(desc(OrderModel.date))
                .all()
            )

            result = []
            for order in orders:
                invoice = (
                    session.query(InvoiceModel)
                    .filter(
                        InvoiceModel.order_id == order.id_key,
                        InvoiceModel.type == InvoiceType.factura,
                    )
                    .first()
                )

                result.append(
                    {
                        "id": order.id_key,
                        "date": order.date,
                        "total": order.final_total,
                        "status": order.status.value if order.status else None,
                        "invoice_number": invoice.number if invoice else None,
                        "invoice_id": invoice.id_key if invoice else None,
                        "payment_method": (
                            order.payment_method.value if order.payment_method else None
                        ),
                        "is_paid": order.is_paid,
                    }
                )

            return result
