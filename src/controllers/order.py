from typing import List, Optional

from fastapi import Depends, HTTPException

from src.controllers.base_implementation import BaseControllerImplementation
from src.models.order import OrderStatus
from src.models.user import UserRole
from src.schemas.order import CreateOrderSchema, ResponseOrderSchema
from src.services.invoice import InvoiceService
from src.services.order import OrderService
from src.utils.rbac import has_role, optional_auth


class OrderController(BaseControllerImplementation):
    def __init__(self):
        super().__init__(
            create_schema=CreateOrderSchema,
            response_schema=ResponseOrderSchema,
            service=OrderService(),
            tags=["Order"],
            required_roles=[
                UserRole.administrador,
                UserRole.cajero,
            ],  # Admin and cashier can access all orders
        )
        self.invoice_service = InvoiceService()

        # Override the default routes with custom implementations
        @self.router.post("/", response_model=ResponseOrderSchema)
        async def create_order(
            order: CreateOrderSchema,
            current_user: Optional[dict] = Depends(optional_auth),
        ):
            # If authenticated, set the user_id from the token
            if current_user:
                order.user_id = current_user["id"]

            # Create order
            return self.service.save(order)

        @self.router.get("/status/{status}", response_model=List[ResponseOrderSchema])
        async def get_by_status(
            status: OrderStatus,
            current_user: dict = Depends(
                has_role([UserRole.administrador, UserRole.cajero, UserRole.cocinero])
            ),
        ):
            return self.service.get_by_status(status)

        @self.router.get("/user/{user_id}", response_model=List[ResponseOrderSchema])
        async def get_by_user(
            user_id: int, current_user: dict = Depends(optional_auth)
        ):
            # If user is requesting their own orders, allow it
            if current_user and str(current_user["id"]) == str(user_id):
                return self.service.get_by_user(user_id)

            # Otherwise, require admin or cashier role
            if not current_user or current_user["role"] not in [
                UserRole.administrador.value,
                UserRole.cajero.value,
            ]:
                raise HTTPException(
                    status_code=403,
                    detail="Not enough permissions to view other users' orders",
                )

            return self.service.get_by_user(user_id)

        @self.router.put("/{id_key}/status", response_model=ResponseOrderSchema)
        async def update_status(
            id_key: int,
            status: OrderStatus,
            current_user: dict = Depends(
                has_role([UserRole.administrador, UserRole.cajero, UserRole.cocinero])
            ),
        ):
            # Different roles can only update to certain statuses
            if current_user["role"] == UserRole.cocinero.value:
                allowed_statuses = [OrderStatus.en_cocina, OrderStatus.listo]
                if status not in allowed_statuses:
                    raise HTTPException(
                        status_code=403,
                        detail=f"Cook can only update status to: "
                        f"{[s.value for s in allowed_statuses]}",
                    )
            elif current_user["role"] == UserRole.delivery.value:
                allowed_statuses = [OrderStatus.en_delivery, OrderStatus.entregado]
                if status not in allowed_statuses:
                    raise HTTPException(
                        status_code=403,
                        detail=f"Delivery can only update status to: "
                        f"{[s.value for s in allowed_statuses]}",
                    )

            return self.service.update_status(id_key, status)

        @self.router.put("/{id_key}/payment", response_model=ResponseOrderSchema)
        async def process_payment(
            id_key: int,
            payment_id: str,
            is_paid: bool = True,
            current_user: dict = Depends(
                has_role([UserRole.administrador, UserRole.cajero])
            ),
        ):
            order = self.service.process_payment(id_key, payment_id, is_paid)

            # Generate invoice if paid
            if is_paid:
                self.invoice_service.generate_invoice(id_key)

            return order
