from fastapi import HTTPException
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

from src.controllers.base_implementation import BaseControllerImplementation
from src.repositories.base_implementation import RecordNotFoundError
from src.schemas.invoice import CreateInvoiceSchema, ResponseInvoiceSchema
from src.services.invoice import InvoiceService


class InvoiceController(BaseControllerImplementation):
    def __init__(self):
        super().__init__(
            create_schema=CreateInvoiceSchema,
            response_schema=ResponseInvoiceSchema,
            service=InvoiceService(),
            tags=["Invoice"],
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
