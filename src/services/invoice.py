import io
import uuid
from datetime import datetime
from typing import Any, Dict

from src.models.invoice import InvoiceModel, InvoiceType
from src.repositories.inventory_item import InventoryItemRepository
from src.repositories.invoice import InvoiceRepository
from src.repositories.manufactured_item import ManufacturedItemRepository
from src.repositories.order import OrderRepository
from src.schemas.invoice import CreateInvoiceSchema, ResponseInvoiceSchema
from src.schemas.invoice_detail import CreateInvoiceDetailSchema
from src.schemas.order import ResponseOrderSchema
from src.services.base_implementation import BaseServiceImplementation
from src.utils.email import send_credit_note_email, send_invoice_email
from src.utils.reportlab import generate_pdf_report


class InvoiceService(BaseServiceImplementation[InvoiceModel, ResponseInvoiceSchema]):
    """Servicio para manejar la lógica de negocio relacionada con las facturas."""

    def __init__(self):
        super().__init__(
            repository=InvoiceRepository(),
            model=InvoiceModel,
            create_schema=CreateInvoiceSchema,
            response_schema=ResponseInvoiceSchema,
        )
        self.order_repository = OrderRepository()
        self.inventory_item_repository = InventoryItemRepository()
        self.manufactured_item_repository = ManufacturedItemRepository()

    async def generate_invoice(self, order_id: int) -> ResponseInvoiceSchema:
        """Genera una factura para un pedido dado."""
        order = self.order_repository.find(order_id)

        invoice_number = (
            f"INV-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        )

        invoice_schema = CreateInvoiceSchema(
            number=invoice_number,
            date=datetime.now(),
            total=order.final_total,
            type=InvoiceType.factura,
            order_id=order_id,
        )

        invoice_details = []

        for detail in order.details:
            invoice_detail = CreateInvoiceDetailSchema(
                item_name=detail.manufactured_item.name,
                quantity=detail.quantity,
                unit_price=detail.unit_price,
                subtotal=detail.subtotal,
                item_type="Manufacturado",
                manufactured_item_id=detail.manufactured_item.id_key,
            )
            invoice_details.append(invoice_detail)

        for detail in order.inventory_details:
            invoice_detail = CreateInvoiceDetailSchema(
                item_name=detail.inventory_item.name,
                quantity=detail.quantity,
                unit_price=detail.unit_price,
                subtotal=detail.subtotal,
                item_type="Insumo",
                inventory_item_id=detail.inventory_item.id_key,
            )
            invoice_details.append(invoice_detail)

        invoice_model = self.to_model(invoice_schema)
        saved_invoice = self.repository.save_with_details(
            invoice_model, invoice_details
        )

        try:
            await self._send_invoice_email(saved_invoice)
        except Exception as e:
            print(f"Error al enviar el correo de la factura: {str(e)}")

        return saved_invoice

    async def generate_credit_note(self, invoice_id: int) -> ResponseInvoiceSchema:
        """Genera una nota de crédito para una factura existente."""
        invoice = self.repository.find(invoice_id)
        self._restore_inventory_stock(invoice.order)

        updated_invoice = self.repository.update(
            invoice_id,
            {
                "number": invoice.number.replace("INV", "NC"),
                "type": InvoiceType.nota_credito,
            },
        )

        try:
            await self._send_credit_note_email(updated_invoice)
        except Exception as e:
            print(f"Error al enviar el correo de la nota de crédito: {str(e)}")

        return updated_invoice

    async def _send_invoice_email(self, invoice: ResponseInvoiceSchema) -> None:
        """Envía un correo electrónico con la factura en formato PDF."""
        invoice_data = self._proces_invoice_details(invoice)
        buffer = io.BytesIO()
        generate_pdf_report(invoice_data, buffer, "Factura")
        pdf_data = buffer.getvalue()
        buffer.close()

        await send_invoice_email(
            customer_email=invoice.order.user.email,
            customer_name=invoice.order.user.full_name,
            invoice_number=invoice.number,
            pdf_data=pdf_data,
        )

    async def _send_credit_note_email(self, invoice: ResponseInvoiceSchema) -> None:
        """Envía un correo electrónico con la nota de crédito en formato PDF."""
        invoice_data = self._proces_invoice_details(invoice)
        buffer = io.BytesIO()
        generate_pdf_report(invoice_data, buffer, "Nota de Crédito")
        pdf_data = buffer.getvalue()
        buffer.close()

        await send_credit_note_email(
            customer_email=invoice.order.user.email,
            customer_name=invoice.order.user.full_name,
            credit_note_number=invoice.number,
            pdf_data=pdf_data,
        )

    @staticmethod
    def _proces_invoice_details(invoice: ResponseInvoiceSchema) -> Dict[str, Any]:
        """Procesa los detalles de la factura para su uso interno."""
        invoice_items = [
            {
                "name": detail.item_name,
                "quantity": detail.quantity,
                "unit_price": detail.unit_price,
                "type": detail.item_type,
                "total": detail.subtotal,
            }
            for detail in invoice.details
        ]

        return {
            "number": invoice.number,
            "date": invoice.date,
            "user_name": invoice.order.user.full_name,
            "items": invoice_items,
            "subtotal": invoice.order.total,
            "discount": invoice.order.discount,
            "total": invoice.total,
        }

    def _restore_inventory_stock(self, order: ResponseOrderSchema) -> None:
        """Restaura el stock de inventario basado en los detalles del pedido."""
        self.inventory_item_repository.restore_inventory_stock(order)
