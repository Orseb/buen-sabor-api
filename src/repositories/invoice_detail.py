from src.models.invoice_detail import InvoiceDetailModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.invoice_detail import (
    CreateInvoiceDetailSchema,
    ResponseInvoiceDetailSchema,
)


class InvoiceDetailRepository(BaseRepositoryImplementation):
    def __init__(self):
        super().__init__(
            model=InvoiceDetailModel,
            create_schema=CreateInvoiceDetailSchema,
            response_schema=ResponseInvoiceDetailSchema,
        )

    def get_by_invoice_id(self, invoice_id: int) -> list[ResponseInvoiceDetailSchema]:
        """Get all details for a specific invoice."""
        with self.session_scope() as session:
            details = (
                session.query(self.model)
                .filter(self.model.invoice_id == invoice_id)
                .filter(self.model.active.is_(True))
                .all()
            )
            return [self.schema.model_validate(detail) for detail in details]
