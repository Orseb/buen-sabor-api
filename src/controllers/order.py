from typing import List

from src.controllers.base_implementation import BaseControllerImplementation
from src.models.order import OrderStatus
from src.schemas.order import CreateOrderSchema, ResponseOrderSchema
from src.services.invoice import InvoiceService
from src.services.order import OrderService


class OrderController(BaseControllerImplementation):
    def __init__(self):
        super().__init__(
            create_schema=CreateOrderSchema,
            response_schema=ResponseOrderSchema,
            service=OrderService(),
            tags=["Order"],
        )
        self.invoice_service = InvoiceService()

        @self.router.get("/status/{status}", response_model=List[ResponseOrderSchema])
        async def get_by_status(status: OrderStatus):
            return self.service.get_by_status(status)

        @self.router.get("/user/{user_id}", response_model=List[ResponseOrderSchema])
        async def get_by_user(user_id: int):
            return self.service.get_by_user(user_id)

        @self.router.put("/{id_key}/status", response_model=ResponseOrderSchema)
        async def update_status(id_key: int, status: OrderStatus):
            return self.service.update_status(id_key, status)

        @self.router.put("/{id_key}/payment", response_model=ResponseOrderSchema)
        async def process_payment(id_key: int, payment_id: str, is_paid: bool = True):
            order = self.service.process_payment(id_key, payment_id, is_paid)

            # Generate invoice if paid
            if is_paid:
                self.invoice_service.generate_invoice(id_key)

            return order
