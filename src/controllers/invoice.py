import io

from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

from src.controllers.base_implementation import BaseControllerImplementation
from src.repositories.base_implementation import RecordNotFoundError
from src.schemas.invoice import CreateInvoiceSchema, ResponseInvoiceSchema
from src.services.invoice import InvoiceService
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
            "/credit-note/{invoice_id}", response_model=ResponseInvoiceSchema
        )
        async def generate_credit_note(invoice_id: int):
            try:
                return self.service.generate_credit_note(invoice_id)
            except RecordNotFoundError as error:
                raise HTTPException(status_code=404, detail=str(error))
            except IntegrityError as error:
                if isinstance(error.orig, UniqueViolation):
                    raise HTTPException(
                        status_code=400, detail="Unique constraint violated."
                    )
                raise HTTPException(
                    status_code=500, detail="An unexpected database error occurred."
                )

        @self.router.get("/report/{id_key}")
        async def get_invoice_report(id_key: int):
            try:
                invoice = self.service.get_one(id_key)
            except RecordNotFoundError as error:
                raise HTTPException(status_code=404, detail=str(error))

            if invoice.original_invoice_id:
                raise HTTPException(
                    status_code=400,
                    detail="Cannot generate report for a credit note invoice.",
                )

            invoice_manufactured_items = [
                {
                    "name": detail.manufactured_item.name,
                    "quantity": detail.quantity,
                    "unit_price": detail.unit_price,
                    "total": detail.subtotal,
                }
                for detail in invoice.order.details
            ]

            invoice_inventory_items = [
                {
                    "name": item.inventory_item.name,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "total": item.subtotal,
                }
                for item in invoice.order.inventory_details
            ]

            invoice_data = {
                "number": invoice.number,
                "date": invoice.date,
                "user_name": invoice.order.user.full_name,
                "items": invoice_manufactured_items + invoice_inventory_items,
                "subtotal": invoice.order.total,
                "discount": invoice.order.discount,
                "total": invoice.total,
            }

            buffer = io.BytesIO()
            generate_pdf_report(invoice_data, buffer, "Factura")
            buffer.seek(0)

            return StreamingResponse(
                buffer,
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f"attachment; filename=invoice_{id_key}.pdf"
                },
            )

        @self.router.get("/note-report/{id_key}")
        async def get_credit_note_report(id_key: int):
            try:
                credit_note = self.service.get_one(id_key)
            except RecordNotFoundError as error:
                raise HTTPException(status_code=404, detail=str(error))

            if not credit_note.original_invoice_id:
                raise HTTPException(
                    status_code=400,
                    detail="This is not a credit note invoice.",
                )

            credit_note_manufactured_items = [
                {
                    "name": detail.manufactured_item.name,
                    "quantity": detail.quantity,
                    "unit_price": detail.unit_price,
                    "total": detail.subtotal,
                }
                for detail in credit_note.order.details
            ]

            credit_note_inventory_items = [
                {
                    "name": item.inventory_item.name,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "total": item.subtotal,
                }
                for item in credit_note.order.inventory_details
            ]

            credit_note_data = {
                "number": credit_note.number,
                "date": credit_note.date,
                "user_name": credit_note.order.user.full_name,
                "items": credit_note_manufactured_items + credit_note_inventory_items,
                "subtotal": credit_note.order.total,
                "discount": credit_note.order.discount,
                "total": credit_note.total,
            }

            buffer = io.BytesIO()
            generate_pdf_report(credit_note_data, buffer, "Nota de Crédito")
            buffer.seek(0)

            return StreamingResponse(
                buffer,
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f"attachment; filename=credit_note_{id_key}.pdf"
                },
            )
