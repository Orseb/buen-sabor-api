from typing import List

from fastapi import Depends, HTTPException

from src.controllers.base_implementation import BaseControllerImplementation
from src.models.order import DeliveryMethod, OrderStatus
from src.models.user import UserRole
from src.schemas.order import CreateOrderSchema, ResponseOrderSchema
from src.services.address import AddressService
from src.services.invoice import InvoiceService
from src.services.order import OrderService
from src.utils.rbac import get_current_user, has_role, optional_auth


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
        self.address_service = AddressService()

        # Override the default routes with custom implementations
        @self.router.post("/generate", response_model=ResponseOrderSchema)
        async def create_order(
            order: CreateOrderSchema, current_user: dict = Depends(get_current_user)
        ):
            # Set the user_id from the token
            order.user_id = current_user["id"]

            # If delivery method is delivery, verify the address belongs to the user

            if order.delivery_method == DeliveryMethod.delivery.value:
                if not order.address_id:
                    raise HTTPException(
                        status_code=400,
                        detail="Delivery orders must have an address",
                    )

                # Verify the address belongs to the user
                try:
                    user_addresses = self.address_service.get_user_addresses(
                        order.user_id
                    )
                    if not any(
                        addr.id_key == order.address_id for addr in user_addresses
                    ):
                        raise HTTPException(
                            status_code=403,
                            detail="The selected address does not belong to the user",
                        )
                except Exception as e:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Error verifying address: {str(e)}",
                    )

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
