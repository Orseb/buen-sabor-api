from typing import List

from src.models.order import DeliveryMethod, OrderModel, OrderStatus
from src.repositories.inventory_item import InventoryItemRepository
from src.repositories.manufactured_item import ManufacturedItemRepository
from src.repositories.order import OrderRepository
from src.repositories.order_detail import OrderDetailRepository
from src.repositories.order_inventory_detail import OrderInventoryDetailRepository
from src.repositories.user import UserRepository
from src.schemas.order import CreateOrderSchema, ResponseOrderSchema
from src.schemas.order_detail import CreateOrderDetailSchema
from src.schemas.order_inventory_detail import CreateOrderInventoryDetailSchema
from src.schemas.pagination import PaginatedResponseSchema
from src.services.base_implementation import BaseServiceImplementation
from src.services.inventory_item import InventoryItemService
from src.services.invoice import InvoiceService
from src.services.manufactured_item import ManufacturedItemService
from src.services.mercado_pago import create_mp_preference


class OrderService(BaseServiceImplementation[OrderModel, ResponseOrderSchema]):
    """Service for order operations."""

    def __init__(self):
        """Initialize the order service with repositories and related services."""
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
        self.manufactured_item_service = ManufacturedItemService()
        self.inventory_item_service = InventoryItemService()
        self.user_repository = UserRepository()

    def save(self, schema: CreateOrderSchema) -> ResponseOrderSchema:
        """Save an order with its details and update inventory stock."""
        details = self._process_details(schema.details)
        inventory_details = self._process_inventory_details(schema.inventory_details)

        schema_dict = schema.model_dump()
        schema_dict.update(
            self._calculate_totals(schema.delivery_method, details, inventory_details)
        )
        schema_dict.pop("details", None)
        schema_dict.pop("inventory_details", None)

        return self.repository.save_with_details(
            OrderModel(**schema_dict), details, inventory_details
        )

    def _process_details(
        self, details: List[CreateOrderDetailSchema]
    ) -> List[CreateOrderDetailSchema]:
        for detail in details:
            detail.unit_price = self.manufactured_item_repository.find(
                detail.manufactured_item_id
            ).price
            detail.subtotal = detail.unit_price * detail.quantity
            self._update_detail_stock(detail)

        return details

    def _process_inventory_details(
        self, inventory_details: List[CreateOrderInventoryDetailSchema]
    ) -> List[CreateOrderInventoryDetailSchema]:
        for detail in inventory_details:
            detail.unit_price = self.inventory_item_repository.find(
                detail.inventory_item_id
            ).price
            detail.subtotal = detail.unit_price * detail.quantity
            self._update_inventory_detail_stock(detail)

        return inventory_details

    def _update_detail_stock(self, detail: CreateOrderDetailSchema) -> None:
        """Update inventory stock based on order details."""
        manufactured_item = self.manufactured_item_repository.find(
            detail.manufactured_item_id
        )
        for item_detail in manufactured_item.details:
            inventory_item = self.inventory_item_service.get_one(
                item_detail.inventory_item.id_key
            )

            quantity_to_subtract = item_detail.quantity * detail.quantity

            if (
                inventory_item.current_stock < quantity_to_subtract
                or inventory_item.current_stock - quantity_to_subtract
                < inventory_item.minimum_stock
            ):
                raise ValueError(f"Insufficient stock for item {inventory_item.name}.")

            new_stock = max(0, inventory_item.current_stock - quantity_to_subtract)

            self.inventory_item_service.update(
                inventory_item.id_key, {"current_stock": new_stock}
            )

    def _update_inventory_detail_stock(
        self, inventory_detail: CreateOrderInventoryDetailSchema
    ) -> None:
        """Update inventory stock based on order inventory details."""
        inventory_item = self.inventory_item_repository.find(
            inventory_detail.inventory_item_id
        )
        quantity_to_subtract = inventory_detail.quantity

        if (
            inventory_item.current_stock < quantity_to_subtract
            or inventory_item.current_stock - quantity_to_subtract
            < inventory_item.minimum_stock
        ):
            raise ValueError(f"Insufficient stock for item {inventory_item.name}.")

        new_stock = max(0, inventory_item.current_stock - quantity_to_subtract)
        self.inventory_item_service.update(
            inventory_item.id_key, {"current_stock": new_stock}
        )

    def _calculate_totals(
        self,
        delivery_method: DeliveryMethod,
        details: List[CreateOrderDetailSchema],
        inventory_details: List[CreateOrderInventoryDetailSchema],
    ) -> dict:
        """Calculate order totals, discount, and final total."""
        total = sum(detail.subtotal for detail in details) + sum(
            inventory_detail.subtotal for inventory_detail in inventory_details
        )
        discount = (
            total * 0.1 if delivery_method == DeliveryMethod.pickup.value else 0.0
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
        """Calculate estimated time for order preparation."""
        items_prep_time = sum(
            self.manufactured_item_repository.find(
                detail.manufactured_item_id
            ).preparation_time
            * detail.quantity
            for detail in order_details
        )

        kitchen_orders = self.repository.find_by_status(
            OrderStatus.en_cocina, offset=0, limit=100
        )
        kitchen_prep_time = sum(order.estimated_time for order in kitchen_orders or [])
        cook_count = self.user_repository.count_all_cookies() or 1

        delivery_time = 10 if delivery_method == DeliveryMethod.delivery.value else 0

        return items_prep_time + (kitchen_prep_time / cook_count) + delivery_time

    def get_by_status(
        self, status: OrderStatus, offset: int = 0, limit: int = 10
    ) -> PaginatedResponseSchema:
        """Get orders by status."""
        total = self.repository.count_all_by_status(status)
        items = self.repository.find_by_status(status, offset, limit)
        return PaginatedResponseSchema(
            total=total, offset=offset, limit=limit, items=items
        )

    def get_by_user(
        self, user_id: int, status: OrderStatus | None, offset: int, limit: int
    ) -> PaginatedResponseSchema:
        """Get orders by user."""
        total = self.repository.count_all_by_user(user_id, status)
        items = self.repository.find_by_user(user_id, status, offset, limit)
        return PaginatedResponseSchema(
            total=total, offset=offset, limit=limit, items=items
        )

    def update_status(self, order_id: int, status: OrderStatus) -> ResponseOrderSchema:
        """Update order status."""
        return self.update(order_id, {"status": status})

    def process_cash_payment(self, order: ResponseOrderSchema) -> ResponseOrderSchema:
        """Process cash payment for an order."""
        self.invoice_service.generate_invoice(order.id_key)
        return self.update(
            order.id_key,
            {
                "payment_id": "Pago en efectivo",
                "is_paid": True,
            },
        )

    def process_mp_payment(self, order: ResponseOrderSchema) -> str:
        """Process Mercado Pago payment for an order."""
        payment_data = create_mp_preference(order)
        self.invoice_service.generate_invoice(order.id_key)

        self.update(
            order.id_key,
            {"payment_id": f"MP-{payment_data['preference_id']}", "is_paid": True},
        )

        return payment_data["payment_url"]

    def add_delay(self, order_id: int, delay_minutes: int) -> ResponseOrderSchema:
        """Add a delay to the estimated time of an order."""
        order = self.get_one(order_id)
        new_estimated_time = order.estimated_time + delay_minutes
        return self.update(order_id, {"estimated_time": new_estimated_time})
