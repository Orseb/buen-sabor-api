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
    """Controlador para manejar las operaciones relacionadas con los pedidos."""

    def __init__(self):
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
            """Genera un nuevo pedido."""
            if (
                not order.details
                and not order.inventory_details
                and not order.promotion_details
            ):
                raise HTTPException(
                    status_code=400,
                    detail="El pedido debe tener al menos un detalle, un insumo o una promoción.",
                )

            for detail in order.inventory_details:
                inventory_item = self.inventory_item_service.get_one(
                    detail.inventory_item_id
                )
                if inventory_item.is_ingredient:
                    raise HTTPException(
                        status_code=400,
                        detail="Los items de inventario deben ser productos, no ingredientes.",
                    )

            order.user_id = current_user["id"]

            if order.delivery_method == DeliveryMethod.pickup.value:
                return self.service.save(order)

            if not order.address_id:
                raise HTTPException(
                    status_code=400,
                    detail="Para pedidos con entrega, se debe proporcionar una direccion.",
                )

            if order.payment_method != PaymentMethod.mercado_pago.value:
                raise HTTPException(
                    status_code=400,
                    detail="Mercado Pago debe ser el metodo de pago para pedidos con entrega.",
                )

            user_addresses = self.address_service.get_all_by(
                "user_id", order.user_id, offset=0, limit=10
            )
            if not any(
                addr.id_key == order.address_id for addr in user_addresses.items
            ):
                raise HTTPException(
                    status_code=403,
                    detail="La direccion seleccionada no pertenece al usuario.",
                )

            return self.service.save(order)

        @self.router.get("/status/{status}", response_model=PaginatedResponseSchema)
        async def get_by_status(
            status: OrderStatus,
            offset: int = 0,
            limit: int = 10,
            _: Dict[str, Any] = Depends(
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
            """Se obtienen los pedidos por estado."""
            return self.service.get_all_by("status", status, offset, limit)

        @self.router.get("/user/token", response_model=PaginatedResponseSchema)
        async def get_by_user(
            user_id: int | None = None,
            status: OrderStatus | None = None,
            offset: int = 0,
            limit: int = 10,
            current_user: Dict[str, Any] = Depends(get_current_user),
        ) -> PaginatedResponseSchema:
            """Se obtienen los pedidos del usuario autenticado o de otro usuario. por id"""
            if not user_id:
                return self.service.get_by_user(
                    current_user["id"], status, offset, limit
                )

            if current_user["role"] != UserRole.administrador.value:
                raise HTTPException(
                    status_code=403,
                    detail="Solo un administrador puede consultar pedidos de otros usuarios.",
                )
            return self.service.get_by_user(user_id, status, offset, limit)

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
            """Actualiza el estado de un pedido."""
            if current_user["role"] == UserRole.cocinero.value:
                allowed_statuses = [
                    OrderStatus.en_cocina.value,
                    OrderStatus.listo.value,
                ]
                if status.value not in allowed_statuses:
                    raise HTTPException(
                        status_code=403,
                        detail=f"El cocinero solo puede actualizar el estado a: {allowed_statuses}",
                    )
            elif current_user["role"] == UserRole.delivery.value:
                allowed_statuses = [
                    OrderStatus.en_delivery.value,
                    OrderStatus.entregado.value,
                ]
                if status.value not in allowed_statuses:
                    raise HTTPException(
                        status_code=403,
                        detail=f"El delivery solo puede actualizar el estado a: {allowed_statuses}",
                    )

            return self.service.update_status(id_key, status)

        @self.router.put("/{id_key}/cash-payment", response_model=ResponseOrderSchema)
        async def process_cash_payment(
            id_key: int,
            _: Dict[str, Any] = Depends(
                has_role([UserRole.cajero, UserRole.administrador])
            ),
        ) -> ResponseOrderSchema:
            """Procesa el pago en efectivo de un pedido."""
            order = self.service.get_one(id_key)

            if order.is_paid:
                raise HTTPException(
                    status_code=403,
                    detail="Este pedido ya ha sido pagado.",
                )

            if order.payment_method != PaymentMethod.cash.value:
                raise HTTPException(
                    status_code=403,
                    detail="Este pedido no acepta efectivo como metodo de pago.",
                )

            return await self.service.process_cash_payment(order)

        @self.router.put("/{id_key}/mp-payment")
        async def process_mp_payment(
            id_key: int,
            _: Dict[str, Any] = Depends(get_current_user),
        ) -> Dict[str, str]:
            """Procesa el pago con Mercado Pago de un pedido."""
            order = self.service.get_one(id_key)

            if order.is_paid:
                raise HTTPException(
                    status_code=403,
                    detail="Este pedido ya ha sido pagado.",
                )

            if order.payment_method != PaymentMethod.mercado_pago.value:
                raise HTTPException(
                    status_code=403,
                    detail="Este pedido no acepta Mercado Pago como metodo de pago.",
                )

            preference_id = await self.service.process_mp_payment(order)

            return {"payment_url": preference_id}

        @self.router.put("/{id_key}/add-delay", response_model=ResponseOrderSchema)
        async def add_delay(
            id_key: int,
            delay_minutes: int,
            _: Dict[str, Any] = Depends(
                has_role([UserRole.administrador, UserRole.cocinero])
            ),
        ) -> ResponseOrderSchema:
            """Agrega retraso en minutos al pedido."""
            if delay_minutes <= 0:
                raise HTTPException(
                    status_code=400,
                    detail="El retraso debe ser mayor a 0 minutos.",
                )
            return self.service.add_delay(id_key, delay_minutes)
