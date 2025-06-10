from typing import Any, Dict

from fastapi import Depends, HTTPException

from src.controllers.base_implementation import BaseControllerImplementation
from src.models.order import DeliveryMethod, OrderStatus, PaymentMethod
from src.models.user import UserRole
from src.schemas.order import CreateOrderSchema, ResponseOrderSchema
from src.schemas.pagination import PaginatedResponseSchema
from src.services.address import AddressService
from src.services.inventory_item import InventoryItemService
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
        self.inventory_item_service = InventoryItemService()

        @self.router.post("/generate", response_model=ResponseOrderSchema)
        async def create_order(
            order: CreateOrderSchema,
            current_user: Dict[str, Any] = Depends(get_current_user),
        ) -> ResponseOrderSchema:
            """Create a new order."""
            if not order.details and not order.inventory_details:
                raise HTTPException(
                    status_code=400,
                    detail="Order must have at least one detail or inventory detail.",
                )

            for detail in order.inventory_details:
                inventory_item = self.inventory_item_service.get_one(
                    detail.inventory_item_id
                )
                if inventory_item.is_ingredient:
                    raise HTTPException(
                        status_code=400,
                        detail="Inventory detail cannot be an ingredient.",
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

            user_addresses = self.address_service.get_all_by(
                "user_id", order.user_id, offset=0, limit=10
            )
            if not any(
                addr.id_key == order.address_id for addr in user_addresses.items
            ):
                raise HTTPException(
                    status_code=403,
                    detail="The selected address does not belong to the user",
                )

            return self.service.save(order)

        @self.router.get("/status/{status}", response_model=PaginatedResponseSchema)
        async def get_by_status(
            status: OrderStatus,
            offset: int = 0,
            limit: int = 10,
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
        ) -> PaginatedResponseSchema:
            """Get orders by status."""
            return self.service.get_by_status(status, offset, limit)

        @self.router.get("/user/token", response_model=PaginatedResponseSchema)
        async def get_by_user(
            offset: int = 0,
            limit: int = 10,
            current_user: Dict[str, Any] = Depends(get_current_user),
        ) -> PaginatedResponseSchema:
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

            return self.service.update_status(id_key, status)

        @self.router.put("/{id_key}/cash-payment", response_model=ResponseOrderSchema)
        async def process_cash_payment(
            id_key: int,
            current_user: Dict[str, Any] = Depends(
                has_role([UserRole.cajero, UserRole.administrador])
            ),
        ) -> ResponseOrderSchema:
            """Process cash payment for an order."""
            order = self.service.get_one(id_key)

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

            return self.service.process_cash_payment(order)

        @self.router.put("/{id_key}/mp-payment")
        async def process_mp_payment(
            id_key: int,
            current_user: Dict[str, Any] = Depends(get_current_user),
        ) -> Dict[str, str]:
            """Process Mercado Pago payment for an order."""
            order = self.service.get_one(id_key)

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
