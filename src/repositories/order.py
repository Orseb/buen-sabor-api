from typing import List

from sqlalchemy import desc

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

    def find_by_status(self, status: OrderStatus) -> List[ResponseOrderSchema]:
        with self.session_scope() as session:
            models = (
                session.query(self.model)
                .filter(self.model.status == status)
                .order_by(desc(self.model.date))
                .all()
            )
            schemas = []
            for model in models:
                schemas.append(self.schema.model_validate(model))
            return schemas

    def find_by_user(self, user_id: int) -> List[ResponseOrderSchema]:
        with self.session_scope() as session:
            models = (
                session.query(self.model)
                .filter(self.model.user_id == user_id)
                .order_by(desc(self.model.date))
                .all()
            )
            schemas = []
            for model in models:
                schemas.append(self.schema.model_validate(model))
            return schemas
