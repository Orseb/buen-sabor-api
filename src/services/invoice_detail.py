from src.models.invoice_detail import InvoiceDetailModel
from src.repositories.invoice_detail import InvoiceDetailRepository
from src.schemas.invoice_detail import (
    CreateInvoiceDetailSchema,
    ResponseInvoiceDetailSchema,
)
from src.services.base_implementation import BaseServiceImplementation


class InvoiceDetailService(BaseServiceImplementation):
    def __init__(self):
        super().__init__(
            repository=InvoiceDetailRepository(),
            model=InvoiceDetailModel,
            create_schema=CreateInvoiceDetailSchema,
            response_schema=ResponseInvoiceDetailSchema,
        )

    def get_by_invoice_id(self, invoice_id: int) -> list[ResponseInvoiceDetailSchema]:
        """Get all details for a specific invoice."""
        return self.repository.get_by_invoice_id(invoice_id)

    def calculate_invoice_total(self, invoice_id: int) -> float:
        """Calculate the total amount for an invoice based on its details."""
        details = self.get_by_invoice_id(invoice_id)
        return sum(detail.subtotal for detail in details)
