from typing import List

from src.models.order import DeliveryMethod, OrderModel, OrderStatus
from src.models.order_detail import OrderDetailModel
from src.models.order_inventory_detail import OrderInventoryDetailModel
from src.repositories.inventory_item import InventoryItemRepository
from src.repositories.manufactured_item import ManufacturedItemRepository
from src.repositories.order import OrderRepository
from src.repositories.order_detail import OrderDetailRepository
from src.repositories.order_inventory_detail import OrderInventoryDetailRepository
from src.schemas.order import CreateOrderSchema, ResponseOrderSchema
from src.schemas.order_detail import CreateOrderDetailSchema
from src.schemas.order_inventory_detail import CreateOrderInventoryDetailSchema
from src.services.base_implementation import BaseServiceImplementation
from src.services.inventory_item import InventoryItemService
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
        self.order_inventory_detail_repository = OrderInventoryDetailRepository()
        self.inventory_item_repository = InventoryItemRepository()
        self.manufactured_item_repository = ManufacturedItemRepository()
        self.manufactured_item_service = ManufacturedItemService()
        self.inventory_item_service = InventoryItemService()

    def save(self, schema: CreateOrderSchema) -> ResponseOrderSchema:
        """Save an order with its details and update inventory stock."""
        details = schema.details
        inventory_details = schema.inventory_details
        schema_dict = schema.model_dump()

        schema_dict["total"] = self._calculate_order_total(details, inventory_details)
        schema_dict["discount"] = (
            schema_dict["total"] * 0.1
            if schema.delivery_method == DeliveryMethod.pickup.value
            else 0.0
        )
        schema_dict["final_total"] = schema_dict["total"] - schema_dict["discount"]

        schema_dict.pop("details", None)
        schema_dict.pop("inventory_details", None)

        order = self.repository.save(OrderModel(**schema_dict))

        self._save_order_details(details, order.id_key)
        self._save_order_inventory_details(inventory_details, order.id_key)
        self._update_inventory_stock(details, order.id_key)

        estimated_time = self._calculate_estimated_time(order.id_key)

        return self.update(order.id_key, {"estimated_time": estimated_time})

    def _calculate_order_total(
        self,
        details: List[CreateOrderDetailSchema],
        inventory_details: List[CreateOrderInventoryDetailSchema],
    ) -> float:
        order_total = 0
        for detail in details:
            order_total += (
                self.manufactured_item_repository.find(
                    detail.manufactured_item_id
                ).price
                * detail.quantity
            )

        for detail in inventory_details:
            order_total += (
                self.inventory_item_repository.find(detail.inventory_item_id).price
                * detail.quantity
            )

        return order_total

    def _save_order_details(
        self, details: List[CreateOrderDetailSchema], order_id: int
    ) -> None:
        """Save order details."""
        for detail in details:
            detail_dict = detail.model_dump()
            detail_dict["order_id"] = order_id
            detail_dict["unit_price"] = self.manufactured_item_repository.find(
                detail.manufactured_item_id
            ).price
            detail_dict["subtotal"] = detail_dict["unit_price"] * detail.quantity
            detail_model = OrderDetailModel(**detail_dict)
            self.order_detail_repository.save(detail_model)

    def _save_order_inventory_details(
        self, inventory_details: List[CreateOrderInventoryDetailSchema], order_id: int
    ) -> None:
        """Save order inventory details."""
        for detail in inventory_details:
            detail_dict = detail.model_dump()
            detail_dict["order_id"] = order_id
            detail_dict["unit_price"] = self.inventory_item_repository.find(
                detail.inventory_item_id
            ).price
            detail_dict["subtotal"] = detail_dict["unit_price"] * detail.quantity
            detail_model = OrderInventoryDetailModel(**detail_dict)
            self.order_inventory_detail_repository.save(detail_model)

    def _update_inventory_stock(
        self, details: List[CreateOrderDetailSchema], order_id: int
    ) -> None:
        """Update inventory stock based on order details."""
        for detail in details:
            manufactured_item = self.manufactured_item_service.get_one(
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
                    raise ValueError(
                        f"Insufficient stock for item {inventory_item.name} in order {order_id}."
                    )

                new_stock = max(0, inventory_item.current_stock - quantity_to_subtract)
                self.inventory_item_service.update(
                    inventory_item.id_key, {"current_stock": new_stock}
                )

    def _calculate_estimated_time(self, order_id: int) -> int:
        """Calculate estimated time for order preparation."""
        order = self.get_one(order_id)

        max_prep_time = 0
        for detail in order.details:
            manufactured_item = self.manufactured_item_service.get_one(
                detail.manufactured_item.id_key
            )
            max_prep_time = max(max_prep_time, manufactured_item.preparation_time)

        orders_in_kitchen = self.get_by_status(OrderStatus.en_cocina)
        kitchen_prep_time = 0
        if orders_in_kitchen:
            for kitchen_order in orders_in_kitchen:
                for detail in kitchen_order.details:
                    manufactured_item = self.manufactured_item_service.get_one(
                        detail.manufactured_item.id_key
                    )
                    kitchen_prep_time = max(
                        kitchen_prep_time, manufactured_item.preparation_time
                    )

        delivery_time = 10 if order.delivery_method == DeliveryMethod.delivery else 0

        total_time = max_prep_time + kitchen_prep_time + delivery_time

        return total_time

    def get_by_status(
        self, status: OrderStatus, offset: int = 0, limit: int = 10
    ) -> List[ResponseOrderSchema]:
        """Get orders by status."""
        return self.repository.find_by_status(status, offset, limit)

    def get_by_user(
        self, user_id: int, offset: int, limit: int
    ) -> List[ResponseOrderSchema]:
        """Get orders by user."""
        return self.repository.find_by_user(user_id, offset, limit)

    def update_status(self, order_id: int, status: OrderStatus) -> ResponseOrderSchema:
        """Update order status."""
        return self.update(order_id, {"status": status})

    def process_cash_payment(self, order: ResponseOrderSchema) -> ResponseOrderSchema:
        """Process cash payment for an order."""
        return self.update(
            order.id_key, {"payment_id": "Pago en efectivo", "is_paid": True}
        )

    def process_mp_payment(self, order: ResponseOrderSchema) -> str:
        """Process Mercado Pago payment for an order."""
        payment_data = create_mp_preference(order)

        self.update(
            order.id_key,
            {"payment_id": f"MP-{payment_data['preference_id']}", "is_paid": True},
        )

        return payment_data["payment_url"]
