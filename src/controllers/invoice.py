import io

from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

from src.controllers.base_implementation import BaseControllerImplementation
from src.repositories.base_implementation import RecordNotFoundError
from src.schemas.invoice import CreateInvoiceSchema, ResponseInvoiceSchema
from src.services.invoice import InvoiceService
from src.utils.reportlab import generate_invoice_pdf


class InvoiceController(BaseControllerImplementation):
    def __init__(self):
        super().__init__(
            create_schema=CreateInvoiceSchema,
            response_schema=ResponseInvoiceSchema,
            service=InvoiceService(),
            tags=["Invoice"],
        )

        @self.router.get("/report/{invoice_id}")
        async def get_invoice_report(invoice_id: int):
            # try:
            #     invoice_data = self.service.get_invoice_data(invoice_id)
            # except RecordNotFoundError as error:
            #     raise HTTPException(status_code=404, detail=str(error))

            invoice_data = {
                "number": "INV-001",
                "date": "2024-06-10",
                "user_name": "John Doe",
                "items": [
                    {
                        "name": "Product A",
                        "quantity": 2,
                        "unit_price": 10.0,
                        "total": 20.0,
                    },
                    {
                        "name": "Product B",
                        "quantity": 1,
                        "unit_price": 15.0,
                        "total": 15.0,
                    },
                ],
                "total": 35.0,
            }

            buffer = io.BytesIO()
            generate_invoice_pdf(invoice_data, buffer)
            buffer.seek(0)

            return StreamingResponse(
                buffer,
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f"attachment; filename=invoice_{invoice_id}.pdf"
                },
            )

        @self.router.post("/generate/{order_id}", response_model=ResponseInvoiceSchema)
        async def generate_invoice(order_id: int):
            try:
                return self.service.generate_invoice(order_id)
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
