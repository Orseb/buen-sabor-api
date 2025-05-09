from typing import List

from src.models.order import DeliveryMethod, OrderModel, OrderStatus, PaymentMethod
from src.models.order_detail import OrderDetailModel
from src.repositories.order import OrderRepository
from src.repositories.order_detail import OrderDetailRepository
from src.schemas.order import CreateOrderSchema, ResponseOrderSchema
from src.schemas.order_detail import CreateOrderDetailSchema
from src.services.base_implementation import BaseServiceImplementation
from src.services.inventory_item import InventoryItemService
from src.services.manufactured_item import ManufacturedItemService


class OrderService(BaseServiceImplementation):
    def __init__(self):
        super().__init__(
            repository=OrderRepository(),
            model=OrderModel,
            create_schema=CreateOrderSchema,
            response_schema=ResponseOrderSchema,
        )
        self.order_detail_repository = OrderDetailRepository()
        self.manufactured_item_service = ManufacturedItemService()
        self.inventory_item_service = InventoryItemService()

    def save(self, schema: CreateOrderSchema) -> ResponseOrderSchema:
        """Save an order with its details"""
        # Apply discount if pickup
        if schema.delivery_method == DeliveryMethod.pickup:
            schema.discount = schema.total * 0.1
            schema.final_total = schema.total - schema.discount

        details = schema.details
        schema.details = []
        order = super().save(schema)

        # Save order details
        for detail in details:
            detail_dict = detail.model_dump()
            detail_dict["order_id"] = order.id_key
            detail_model = OrderDetailModel(**detail_dict)
            self.order_detail_repository.save(detail_model)

        # Update inventory stock
        self._update_inventory_stock(details, order.id_key)

        # Calculate estimated time
        estimated_time = self._calculate_estimated_time(order.id_key)
        self.update(order.id_key, {"estimated_time": estimated_time})

        return self.get_one(order.id_key)

    def _update_inventory_stock(
        self, details: List[CreateOrderDetailSchema], order_id: int
    ) -> None:
        """Update inventory stock based on order details"""
        for detail in details:
            manufactured_item = self.manufactured_item_service.get_one(
                detail.manufactured_item_id
            )

            for item_detail in manufactured_item.details:
                inventory_item = self.inventory_item_service.get_one(
                    item_detail.inventory_item.id_key
                )

                # Calculate quantity to subtract
                quantity_to_subtract = item_detail.quantity * detail.quantity

                # Update inventory stock
                new_stock = inventory_item.current_stock - quantity_to_subtract
                self.inventory_item_service.update(
                    inventory_item.id_key, {"current_stock": new_stock}
                )

    def _calculate_estimated_time(self, order_id: int) -> int:
        """Calculate estimated time for order preparation"""
        order = self.get_one(order_id)

        # Get max preparation time from ordered items
        max_prep_time = 0
        for detail in order.details:
            manufactured_item = self.manufactured_item_service.get_one(
                detail.manufactured_item.id_key
            )
            max_prep_time = max(max_prep_time, manufactured_item.preparation_time)

        # Get max preparation time from orders in kitchen
        orders_in_kitchen = self.get_by_status(OrderStatus.en_cocina)
        kitchen_prep_time = 0
        for kitchen_order in orders_in_kitchen:
            for detail in kitchen_order.details:
                manufactured_item = self.manufactured_item_service.get_one(
                    detail.manufactured_item.id_key
                )
                kitchen_prep_time = max(
                    kitchen_prep_time, manufactured_item.preparation_time
                )

        # Add delivery time if applicable
        delivery_time = 10 if order.delivery_method == DeliveryMethod.delivery else 0

        # Calculate total estimated time
        total_time = max_prep_time + kitchen_prep_time + delivery_time

        return total_time

    def get_by_status(self, status: OrderStatus) -> List[ResponseOrderSchema]:
        """Get orders by status"""
        return self.repository.find_by_status(status)

    def get_by_user(self, user_id: int) -> List[ResponseOrderSchema]:
        """Get orders by user"""
        return self.repository.find_by_user(user_id)

    def update_status(self, order_id: int, status: OrderStatus) -> ResponseOrderSchema:
        """Update order status"""
        return self.update(order_id, {"status": status})

    def process_payment(
        self, order_id: int, payment_method: PaymentMethod
    ) -> ResponseOrderSchema:
        """Process payment for an order"""
        if payment_method == PaymentMethod.cash.value:
            return self.update(
                order_id, {"payment_id": "Pago en efectivo", "is_paid": True}
            )

        return self.update(
            order_id, {"payment_id": "Pago con Mercado Pago", "is_paid": True}
        )
