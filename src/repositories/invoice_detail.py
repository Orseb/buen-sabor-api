from src.models.invoice_detail import InvoiceDetailModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.invoice_detail import (
    CreateInvoiceDetailSchema,
    ResponseInvoiceDetailSchema,
)


class InvoiceDetailRepository(BaseRepositoryImplementation):
    """Repositorio para manejar las operaciones de detalles de factura."""

    def __init__(self):
        super().__init__(
            model=InvoiceDetailModel,
            create_schema=CreateInvoiceDetailSchema,
            response_schema=ResponseInvoiceDetailSchema,
        )
