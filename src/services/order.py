from typing import Dict, List

from src.config.settings import settings
from src.models.order import DeliveryMethod, OrderModel, OrderStatus
from src.repositories.inventory_item import InventoryItemRepository
from src.repositories.manufactured_item import ManufacturedItemRepository
from src.repositories.order import OrderRepository
from src.repositories.order_detail import OrderDetailRepository
from src.repositories.order_inventory_detail import OrderInventoryDetailRepository
from src.repositories.promotion import PromotionRepository
from src.repositories.user import UserRepository
from src.schemas.order import CreateOrderSchema, ResponseOrderSchema
from src.schemas.order_detail import CreateOrderDetailSchema
from src.schemas.order_inventory_detail import CreateOrderInventoryDetailSchema
from src.schemas.order_promotion_detail import CreateOrderPromotionDetailSchema
from src.schemas.pagination import PaginatedResponseSchema
from src.services.base_implementation import BaseServiceImplementation
from src.services.invoice import InvoiceService
from src.services.mercado_pago import create_mp_preference


class OrderService(BaseServiceImplementation[OrderModel, ResponseOrderSchema]):
    """Servicio para operaciones relacionadas con pedidos."""

    def __init__(self):
        super().__init__(
            repository=OrderRepository(),
            model=OrderModel,
            create_schema=CreateOrderSchema,
            response_schema=ResponseOrderSchema,
        )
        self.order_detail_repository = OrderDetailRepository()
        self.invoice_service = InvoiceService()
        self.order_inventory_detail_repository = OrderInventoryDetailRepository()
        self.inventory_item_repository = InventoryItemRepository()
        self.manufactured_item_repository = ManufacturedItemRepository()
        self.promotion_repository = PromotionRepository()
        self.user_repository = UserRepository()

    def save(self, schema: CreateOrderSchema) -> ResponseOrderSchema:
        """Guarda un nuevo pedido con sus detalles y calcula totales."""
        expanded_details, expanded_inventory_details = self._expand_promotions(
            schema.promotion_details
        )

        all_details = schema.details + expanded_details
        all_inventory_details = schema.inventory_details + expanded_inventory_details

        details = self._process_details(all_details)
        inventory_details = self._process_inventory_details(all_inventory_details)

        schema_dict = schema.model_dump()
        schema_dict.update(
            self._calculate_totals(schema.delivery_method, details, inventory_details)
        )
        schema_dict.pop("details", None)
        schema_dict.pop("inventory_details", None)
        schema_dict.pop("promotion_details", None)

        return self.repository.save_with_details(
            OrderModel(**schema_dict), details, inventory_details
        )

    def _expand_promotions(
        self, promotion_details: List[CreateOrderPromotionDetailSchema]
    ) -> tuple[List[CreateOrderDetailSchema], List[CreateOrderInventoryDetailSchema]]:
        """Expande las promociones en detalles regulares de pedido."""
        expanded_details = []
        expanded_inventory_details = []

        for promotion_detail in promotion_details:
            promotion = self.promotion_repository.find(promotion_detail.promotion_id)
            discount_multiplier = 1 - (promotion.discount_percentage / 100)

            for manufactured_detail in promotion.manufactured_item_details:
                original_price = manufactured_detail.manufactured_item.price
                discounted_price = original_price * discount_multiplier
                total_quantity = (
                    manufactured_detail.quantity * promotion_detail.quantity
                )

                existing_detail = next(
                    (
                        detail
                        for detail in expanded_details
                        if detail.manufactured_item_id
                        == manufactured_detail.manufactured_item.id_key
                    ),
                    None,
                )

                if existing_detail:
                    current_total_value = (
                        existing_detail.unit_price * existing_detail.quantity
                    )
                    new_total_value = discounted_price * total_quantity
                    combined_quantity = existing_detail.quantity + total_quantity

                    existing_detail.unit_price = (
                        current_total_value + new_total_value
                    ) / combined_quantity
                    existing_detail.quantity = combined_quantity
                    existing_detail.subtotal = (
                        existing_detail.unit_price * existing_detail.quantity
                    )
                else:
                    expanded_detail = CreateOrderDetailSchema(
                        manufactured_item_id=manufactured_detail.manufactured_item.id_key,
                        quantity=total_quantity,
                        unit_price=discounted_price,
                        subtotal=discounted_price * total_quantity,
                    )
                    expanded_details.append(expanded_detail)

            for inventory_detail in promotion.inventory_item_details:
                original_price = inventory_detail.inventory_item.price
                discounted_price = original_price * discount_multiplier
                total_quantity = inventory_detail.quantity * promotion_detail.quantity

                existing_detail = next(
                    (
                        detail
                        for detail in expanded_inventory_details
                        if detail.inventory_item_id
                        == inventory_detail.inventory_item.id_key
                    ),
                    None,
                )

                if existing_detail:
                    current_total_value = (
                        existing_detail.unit_price * existing_detail.quantity
                    )
                    new_total_value = discounted_price * total_quantity
                    combined_quantity = existing_detail.quantity + total_quantity

                    existing_detail.unit_price = (
                        current_total_value + new_total_value
                    ) / combined_quantity
                    existing_detail.quantity = combined_quantity
                    existing_detail.subtotal = (
                        existing_detail.unit_price * existing_detail.quantity
                    )
                else:
                    expanded_inventory_detail = CreateOrderInventoryDetailSchema(
                        inventory_item_id=inventory_detail.inventory_item.id_key,
                        quantity=total_quantity,
                        unit_price=discounted_price,
                        subtotal=discounted_price * total_quantity,
                    )
                    expanded_inventory_details.append(expanded_inventory_detail)

        return expanded_details, expanded_inventory_details

    def _process_details(
        self, details: List[CreateOrderDetailSchema]
    ) -> List[CreateOrderDetailSchema]:
        """Procesa los detalles de los items manufacturados y actualiza el stock."""
        for detail in details:
            if detail.unit_price is None:
                detail.unit_price = self.manufactured_item_repository.find(
                    detail.manufactured_item_id
                ).price
            if detail.subtotal is None:
                detail.subtotal = detail.unit_price * detail.quantity
            self._update_detail_stock(detail)

        return details

    def _process_inventory_details(
        self, inventory_details: List[CreateOrderInventoryDetailSchema]
    ) -> List[CreateOrderInventoryDetailSchema]:
        """Procesa los detalles de inventario y actualiza el stock."""
        for detail in inventory_details:
            if detail.unit_price is None:
                detail.unit_price = self.inventory_item_repository.find(
                    detail.inventory_item_id
                ).price
            if detail.subtotal is None:
                detail.subtotal = detail.unit_price * detail.quantity
            self._update_inventory_detail_stock(detail)

        return inventory_details

    def _update_detail_stock(self, detail: CreateOrderDetailSchema) -> None:
        """Actualiza el stock de los items manufacturados."""
        manufactured_item = self.manufactured_item_repository.find(
            detail.manufactured_item_id
        )
        for item_detail in manufactured_item.details:
            quantity_to_subtract = item_detail.quantity * detail.quantity

            if item_detail.inventory_item.current_stock < quantity_to_subtract:
                raise ValueError(
                    f"Stock insuficiente para el item {item_detail.inventory_item.name}."
                )

            self.inventory_item_repository.update(
                item_detail.inventory_item.id_key,
                {
                    "current_stock": item_detail.inventory_item.current_stock
                    - quantity_to_subtract
                },
            )

    def _update_inventory_detail_stock(
        self, inventory_detail: CreateOrderInventoryDetailSchema
    ) -> None:
        """Actualiza el stock de los items de inventario."""
        inventory_item = self.inventory_item_repository.find(
            inventory_detail.inventory_item_id
        )
        quantity_to_subtract = inventory_detail.quantity

        if inventory_item.current_stock < quantity_to_subtract:
            raise ValueError(f"Stock insuficiente para el item {inventory_item.name}.")

        self.inventory_item_repository.update(
            inventory_item.id_key,
            {"current_stock": inventory_item.current_stock - quantity_to_subtract},
        )

    def _calculate_totals(
        self,
        delivery_method: DeliveryMethod,
        details: List[CreateOrderDetailSchema],
        inventory_details: List[CreateOrderInventoryDetailSchema],
    ) -> Dict[str, float]:
        """Calcula el total, descuento y tiempo estimado del pedido."""
        total = sum(detail.subtotal for detail in details) + sum(
            inventory_detail.subtotal for inventory_detail in inventory_details
        )
        discount = (
            total * settings.pickup_discount
            if delivery_method == DeliveryMethod.pickup.value
            else 0.0
        )
        final_total = total - discount
        estimated_time = self._calculate_estimated_time(delivery_method, details)
        return {
            "total": total,
            "discount": discount,
            "final_total": final_total,
            "estimated_time": estimated_time,
        }

    def _calculate_estimated_time(
        self,
        delivery_method: DeliveryMethod,
        order_details: List[CreateOrderDetailSchema],
    ) -> float:
        """Calcula el tiempo estimado de preparación del pedido."""
        if not order_details:
            return 0.0

        items_prep_time = sum(
            self.manufactured_item_repository.find(
                detail.manufactured_item_id
            ).preparation_time
            * detail.quantity
            for detail in order_details
        )

        kitchen_orders = self.repository.find_all_by(
            "status", OrderStatus.en_cocina, offset=0, limit=100
        )
        kitchen_prep_time = sum(order.estimated_time for order in kitchen_orders or [])
        cook_count = self.user_repository.count_all_cookies() or 1

        delivery_time = 10 if delivery_method == DeliveryMethod.delivery.value else 0

        return items_prep_time + (kitchen_prep_time / cook_count) + delivery_time

    def get_by_user(
        self, user_id: int, status: OrderStatus | None, offset: int, limit: int
    ) -> PaginatedResponseSchema:
        """Obtiene los pedidos de un usuario con paginación y filtrado por estado."""
        total = self.repository.count_all_by_user(user_id, status)
        items = self.repository.find_by_user(user_id, status, offset, limit)
        return PaginatedResponseSchema(
            total=total, offset=offset, limit=limit, items=items
        )

    def update_status(self, order_id: int, status: OrderStatus) -> ResponseOrderSchema:
        """Actualiza el estado de un pedido."""
        return self.repository.update(order_id, {"status": status})

    async def process_cash_payment(
        self, order: ResponseOrderSchema
    ) -> ResponseOrderSchema:
        """Procesa el pago en efectivo de un pedido."""
        await self.invoice_service.generate_invoice(order.id_key)
        return self.repository.update(
            order.id_key,
            {
                "payment_id": "Pago en efectivo",
                "is_paid": True,
            },
        )

    async def process_mp_payment(self, order: ResponseOrderSchema) -> str:
        """Procesa el pago con Mercado Pago para un pedido."""
        payment_data = create_mp_preference(order)
        await self.invoice_service.generate_invoice(order.id_key)

        self.repository.update(
            order.id_key,
            {"payment_id": f"MP-{payment_data['preference_id']}", "is_paid": True},
        )

        return payment_data["payment_url"]

    def add_delay(self, order_id: int, delay_minutes: int) -> ResponseOrderSchema:
        """Agrega un retraso al tiempo estimado de un pedido."""
        order = self.repository.find(order_id)
        new_estimated_time = order.estimated_time + delay_minutes
        return self.repository.update(order_id, {"estimated_time": new_estimated_time})

    def search_orders_by_id(
        self, search_term: str, offset: int = 0, limit: int = 10
    ) -> PaginatedResponseSchema:
        """Busca órdenes por ID con paginación."""
        total = self.repository.count_search_orders_by_id(search_term)
        items = self.repository.search_orders_by_id(search_term, offset, limit)
        return PaginatedResponseSchema(
            total=total, offset=offset, limit=limit, items=items
        )
