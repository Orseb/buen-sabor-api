from src.models.inventory_item import InventoryItemModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.inventory_item import (
    CreateInventoryItemSchema,
    ResponseInventoryItemSchema,
)
from src.schemas.order import ResponseOrderSchema


class InventoryItemRepository(BaseRepositoryImplementation):
    """Repositorio para manejo de artículos de inventario."""

    def __init__(self):
        super().__init__(
            model=InventoryItemModel,
            create_schema=CreateInventoryItemSchema,
            response_schema=ResponseInventoryItemSchema,
        )

    def restore_inventory_stock(self, order: ResponseOrderSchema) -> None:
        """Restaura el stock de inventario basado en los detalles del pedido."""
        with self.session_scope() as session:
            for detail in order.details:
                for manufactured_item_detail in detail.manufactured_item.details:
                    quantity_to_add = (
                        manufactured_item_detail.quantity * detail.quantity
                    )

                    inventory_item = session.get(
                        self.model, manufactured_item_detail.inventory_item.id_key
                    )

                    if inventory_item:
                        inventory_item.current_stock += quantity_to_add

            for detail in order.inventory_details:
                inventory_item = session.get(self.model, detail.inventory_item.id_key)

                if inventory_item:
                    inventory_item.current_stock += detail.quantity
