import io

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from src.models.invoice import InvoiceType
from src.models.user import UserRole
from src.schemas.invoice import ResponseInvoiceSchema
from src.schemas.pagination import PaginatedResponseSchema
from src.services.invoice import InvoiceService
from src.utils.rbac import get_current_user, has_role
from src.utils.reportlab import generate_pdf_report


class InvoiceController:
    """Controlador para manejar las facturas y notas de crédito."""

    def __init__(self):
        self.router = APIRouter(tags=["Invoice"])
        self.service = InvoiceService()

        @self.router.get("/", response_model=PaginatedResponseSchema)
        async def get_all_invoices(
            offset: int = 0,
            limit: int = 10,
            _: dict = Depends(has_role([UserRole.administrador, UserRole.cajero])),
        ) -> PaginatedResponseSchema:
            """Obtiene todas las facturas y notas de crédito."""
            return self.service.get_all(offset, limit)

        @self.router.post(
            "/credit-note/{id_key}",
            response_model=ResponseInvoiceSchema,
        )
        async def generate_credit_note(
            id_key: int,
            _: dict = Depends(has_role([UserRole.administrador, UserRole.cajero])),
        ) -> ResponseInvoiceSchema:
            """Genera una nota de crédito a partir de una factura existente."""
            return await self.service.generate_credit_note(id_key)

        @self.router.get("/report/{id_key}")
        async def get_invoice_report(
            id_key: int, _: dict = Depends(get_current_user)
        ) -> StreamingResponse:
            """Genera un reporte PDF de la factura o nota de crédito."""
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

            report_type = (
                "Factura"
                if invoice.type == InvoiceType.factura.value
                else "Nota de Crédito"
            )
            filename = (
                f"{'invoice' if invoice.type == InvoiceType.factura.value else 'credit_note'}"
                f"_{id_key}.pdf"
            )

            buffer = io.BytesIO()
            generate_pdf_report(invoice_data, buffer, report_type)
            buffer.seek(0)

            return StreamingResponse(
                buffer,
                media_type="application/pdf",
                headers={"Content-Disposition": f"attachment; filename={filename}"},
            )

        @self.router.get("/search", response_model=PaginatedResponseSchema)
        async def search_invoices(
            search_term: str,
            offset: int = 0,
            limit: int = 10,
            _: dict = Depends(has_role([UserRole.administrador, UserRole.cajero])),
        ) -> PaginatedResponseSchema:
            """Busca facturas por número."""
            return self.service.search_invoices_by_number(search_term, offset, limit)
