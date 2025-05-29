from typing import Any, Dict, List

from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from src.controllers.base_implementation import BaseControllerImplementation
from src.models.order import DeliveryMethod, OrderStatus, PaymentMethod
from src.models.user import UserRole
from src.repositories.base_implementation import RecordNotFoundError
from src.schemas.order import CreateOrderSchema, ResponseOrderSchema
from src.services.address import AddressService
from src.services.invoice import InvoiceService
from src.services.order import OrderService
from src.utils.rbac import get_current_user, has_role


class OrderController(
    BaseControllerImplementation[ResponseOrderSchema, CreateOrderSchema]
):
    """Controller for order endpoints."""

    def __init__(self):
        """Initialize the order controller with service and schemas."""
        super().__init__(
            create_schema=CreateOrderSchema,
            response_schema=ResponseOrderSchema,
            service=OrderService(),
            tags=["Order"],
            required_roles=[
                UserRole.administrador,
                UserRole.cajero,
                UserRole.delivery,
                UserRole.cocinero,
            ],
        )
        self.invoice_service = InvoiceService()
        self.address_service = AddressService()

        @self.router.post("/generate", response_model=ResponseOrderSchema)
        async def create_order(
            order: CreateOrderSchema,
            current_user: Dict[str, Any] = Depends(get_current_user),
        ) -> ResponseOrderSchema:
            """Create a new order."""
            try:
                if not order.details and not order.inventory_details:
                    raise HTTPException(
                        status_code=400,
                        detail="Order must have at least one detail or inventory detail.",
                    )

                order.user_id = current_user["id"]

                if order.delivery_method == DeliveryMethod.pickup.value:
                    return self.service.save(order)

                if not order.address_id:
                    raise HTTPException(
                        status_code=400,
                        detail="An address must be supplied in delivery method.",
                    )

                if order.payment_method != PaymentMethod.mercado_pago.value:
                    raise HTTPException(
                        status_code=400,
                        detail="Mercado Pago must be selected as the payment method in delivery.",
                    )

                user_addresses = self.address_service.get_user_addresses(order.user_id)
                if not any(addr.id_key == order.address_id for addr in user_addresses):
                    raise HTTPException(
                        status_code=403,
                        detail="The selected address does not belong to the user",
                    )

                return self.service.save(order)
            except ValueError as error:
                raise HTTPException(status_code=400, detail=str(error))

        @self.router.get("/status/{status}", response_model=List[ResponseOrderSchema])
        async def get_by_status(
            status: OrderStatus,
            offset: int = 0,
            limit: int = 10,
            current_user: Dict[str, Any] = Depends(
                has_role([UserRole.administrador, UserRole.cajero, UserRole.cocinero])
            ),
        ) -> List[ResponseOrderSchema]:
            """Get orders by status."""
            return self.service.get_by_status(status, offset, limit)

        @self.router.get("/user/token", response_model=List[ResponseOrderSchema])
        async def get_by_user(
            offset: int = 0,
            limit: int = 10,
            current_user: Dict[str, Any] = Depends(get_current_user),
        ) -> List[ResponseOrderSchema]:
            """Get orders by user."""
            return self.service.get_by_user(current_user["id"], offset, limit)

        @self.router.put("/{id_key}/status", response_model=ResponseOrderSchema)
        async def update_status(
            id_key: int,
            status: OrderStatus,
            current_user: Dict[str, Any] = Depends(
                has_role(
                    [
                        UserRole.administrador,
                        UserRole.cajero,
                        UserRole.cocinero,
                        UserRole.delivery,
                    ]
                )
            ),
        ) -> ResponseOrderSchema:
            """Update order status."""
            if current_user["role"] == UserRole.cocinero.value:
                allowed_statuses = [
                    OrderStatus.en_cocina.value,
                    OrderStatus.listo.value,
                ]
                if status.value not in allowed_statuses:
                    raise HTTPException(
                        status_code=403,
                        detail=f"Cook can only update status to: {allowed_statuses}",
                    )
            elif current_user["role"] == UserRole.delivery.value:
                allowed_statuses = [
                    OrderStatus.en_delivery.value,
                    OrderStatus.entregado.value,
                ]
                if status.value not in allowed_statuses:
                    raise HTTPException(
                        status_code=403,
                        detail=f"Delivery can only update status to: {allowed_statuses}",
                    )

            try:
                return self.service.update_status(id_key, status)
            except RecordNotFoundError as error:
                raise HTTPException(status_code=404, detail=str(error))
            except IntegrityError:
                raise HTTPException(
                    status_code=500, detail="An unexpected database error occurred."
                )

        @self.router.put("/{id_key}/cash-payment", response_model=ResponseOrderSchema)
        async def process_cash_payment(
            id_key: int,
            current_user: Dict[str, Any] = Depends(
                has_role([UserRole.cajero, UserRole.administrador])
            ),
        ) -> ResponseOrderSchema:
            """Process cash payment for an order."""
            try:
                order = self.service.get_one(id_key)
            except RecordNotFoundError as error:
                raise HTTPException(status_code=404, detail=str(error))
            except IntegrityError:
                raise HTTPException(
                    status_code=500, detail="An unexpected database error occurred."
                )

            if order.is_paid:
                raise HTTPException(
                    status_code=403,
                    detail="This order has already been paid.",
                )

            if order.payment_method != PaymentMethod.cash.value:
                raise HTTPException(
                    status_code=403,
                    detail="This order does not accept cash as the payment method.",
                )

            paid_order = self.service.process_cash_payment(order)

            self.invoice_service.generate_invoice(order.id_key)

            return paid_order

        @self.router.put("/{id_key}/mp-payment")
        async def process_mp_payment(
            id_key: int,
            current_user: Dict[str, Any] = Depends(get_current_user),
        ) -> Dict[str, str]:
            """Process Mercado Pago payment for an order."""
            try:
                order = self.service.get_one(id_key)
            except RecordNotFoundError as error:
                raise HTTPException(status_code=404, detail=str(error))
            except IntegrityError:
                raise HTTPException(
                    status_code=500, detail="An unexpected database error occurred."
                )

            if order.is_paid:
                raise HTTPException(
                    status_code=403,
                    detail="This order has already been paid.",
                )

            if order.payment_method != PaymentMethod.mercado_pago.value:
                raise HTTPException(
                    status_code=403,
                    detail="This order does not accept MP as the payment method.",
                )

            preference_id = self.service.process_mp_payment(order)

            return {"payment_url": preference_id}
