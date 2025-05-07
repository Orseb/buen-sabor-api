from typing import Optional

from src.controllers.base_implementation import BaseControllerImplementation
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
            return self.service.generate_invoice(order_id)

        @self.router.post(
            "/credit-note/{invoice_id}", response_model=ResponseInvoiceSchema
        )
        async def generate_credit_note(invoice_id: int, reason: Optional[str] = None):
            return self.service.generate_credit_note(invoice_id, reason)
