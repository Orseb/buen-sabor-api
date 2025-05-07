from src.models.invoice import InvoiceModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.invoice import CreateInvoiceSchema, ResponseInvoiceSchema


class InvoiceRepository(BaseRepositoryImplementation):
    def __init__(self):
        super().__init__(
            model=InvoiceModel,
            create_schema=CreateInvoiceSchema,
            response_schema=ResponseInvoiceSchema,
        )
