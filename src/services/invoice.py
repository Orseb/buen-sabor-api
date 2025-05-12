import uuid
from datetime import datetime

from src.models.invoice import InvoiceModel, InvoiceType
from src.repositories.invoice import InvoiceRepository
from src.schemas.invoice import CreateInvoiceSchema, ResponseInvoiceSchema
from src.services.base_implementation import BaseServiceImplementation


class InvoiceService(BaseServiceImplementation[InvoiceModel, ResponseInvoiceSchema]):
    """Service for invoice operations."""

    def __init__(self):
        """Initialize the invoice service with repository and related services."""
        super().__init__(
            repository=InvoiceRepository(),
            model=InvoiceModel,
            create_schema=CreateInvoiceSchema,
            response_schema=ResponseInvoiceSchema,
        )
        self._order_service = None
        self._inventory_item_service = None

    @property
    def order_service(self):
        """Lazy-loaded order service to avoid circular imports."""
        if self._order_service is None:
            from src.services.order import OrderService

            self._order_service = OrderService()
        return self._order_service

    @property
    def inventory_item_service(self):
        """Lazy-loaded inventory item service to avoid circular imports."""
        if self._inventory_item_service is None:
            from src.services.inventory_item import InventoryItemService

            self._inventory_item_service = InventoryItemService()
        return self._inventory_item_service

    def generate_invoice(self, order_id: int) -> ResponseInvoiceSchema:
        """Generate an invoice for an order."""
        order = self.order_service.get_one(order_id)

        invoice_number = (
            f"INV-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        )

        invoice = self.save(
            CreateInvoiceSchema(
                number=invoice_number,
                date=datetime.now(),
                total=order.final_total,
                type=InvoiceType.factura,
                order_id=order_id,
            )
        )

        self.order_service.update_status(order_id, "facturado")

        return invoice

    def generate_credit_note(self, invoice_id: int) -> ResponseInvoiceSchema:
        """Generate a credit note for an invoice."""
        invoice = self.get_one(invoice_id)
        order = self.order_service.get_one(invoice.order.id_key)

        credit_note_number = (
            f"NC-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        )

        credit_note = self.save(
            CreateInvoiceSchema(
                number=credit_note_number,
                date=datetime.now(),
                total=invoice.total,
                type=InvoiceType.nota_credito,
                order_id=order.id_key,
                original_invoice_id=invoice_id,
            )
        )

        self._restore_inventory_stock(order.id_key)

        return credit_note

    def _restore_inventory_stock(self, order_id: int) -> None:
        """Restore inventory stock based on order details."""
        order = self.order_service.get_one(order_id)

        for detail in order.details:
            from src.services.manufactured_item import ManufacturedItemService

            manufactured_item_service = ManufacturedItemService()

            manufactured_item = manufactured_item_service.get_one(
                detail.manufactured_item.id_key
            )

            for item_detail in manufactured_item.details:
                inventory_item = self.inventory_item_service.get_one(
                    item_detail.inventory_item.id_key
                )

                quantity_to_add = item_detail.quantity * detail.quantity

                new_stock = inventory_item.current_stock + quantity_to_add
                self.inventory_item_service.update(
                    inventory_item.id_key, {"current_stock": new_stock}
                )
