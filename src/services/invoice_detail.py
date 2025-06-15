from src.models.invoice_detail import InvoiceDetailModel
from src.repositories.invoice_detail import InvoiceDetailRepository
from src.schemas.invoice_detail import (
    CreateInvoiceDetailSchema,
    ResponseInvoiceDetailSchema,
)
from src.services.base_implementation import BaseServiceImplementation


class InvoiceDetailService(BaseServiceImplementation):
    """Servicio para manejar la lógica de negocio relacionada con los detalles de las facturas."""

    def __init__(self):
        super().__init__(
            repository=InvoiceDetailRepository(),
            model=InvoiceDetailModel,
            create_schema=CreateInvoiceDetailSchema,
            response_schema=ResponseInvoiceDetailSchema,
        )
