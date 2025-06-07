import io

from fastapi import Depends
from fastapi.responses import StreamingResponse

from src.controllers.base_implementation import BaseControllerImplementation
from src.models.invoice import InvoiceType
from src.schemas.invoice import CreateInvoiceSchema, ResponseInvoiceSchema
from src.services.invoice import InvoiceService
from src.utils.rbac import get_current_user
from src.utils.reportlab import generate_pdf_report


class InvoiceController(BaseControllerImplementation):
    def __init__(self):
        super().__init__(
            create_schema=CreateInvoiceSchema,
            response_schema=ResponseInvoiceSchema,
            service=InvoiceService(),
            tags=["Invoice"],
        )

        @self.router.post(
            "/credit-note/{id_key}",
            response_model=ResponseInvoiceSchema,
        )
        async def generate_credit_note(
            id_key: int, current_user: dict = Depends(get_current_user)
        ):
            return self.service.generate_credit_note(id_key)

        @self.router.get("/report/{id_key}")
        async def get_invoice_report(
            id_key: int, current_user: dict = Depends(get_current_user)
        ):
            invoice = self.service.get_one(id_key)

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

            invoice_data = {
                "number": invoice.number,
                "date": invoice.date,
                "user_name": invoice.order.user.full_name,
                "items": invoice_items,
                "subtotal": invoice.order.total,
                "discount": invoice.order.discount,
                "total": invoice.total,
            }

            buffer = io.BytesIO()

            if invoice.type == InvoiceType.factura.value:
                generate_pdf_report(invoice_data, buffer, "Factura")
                filename = f"invoice_{id_key}.pdf"
            else:
                generate_pdf_report(invoice_data, buffer, "Nota de Crédito")
                filename = f"credit_note_{id_key}.pdf"

            buffer.seek(0)

            return StreamingResponse(
                buffer,
                media_type="application/pdf",
                headers={"Content-Disposition": f"attachment; filename={filename}"},
            )
