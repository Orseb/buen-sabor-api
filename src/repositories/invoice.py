from src.models.invoice import InvoiceModel
from src.models.invoice_detail import InvoiceDetailModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.invoice import CreateInvoiceSchema, ResponseInvoiceSchema


class InvoiceRepository(BaseRepositoryImplementation):
    def __init__(self):
        super().__init__(
            model=InvoiceModel,
            create_schema=CreateInvoiceSchema,
            response_schema=ResponseInvoiceSchema,
        )

    def save_with_details(self, invoice_model, details) -> ResponseInvoiceSchema:
        """Save an invoice along with its details."""
        with self.session_scope() as session:
            session.add(invoice_model)
            session.flush()

            for detail in details:
                detail_dict = detail.model_dump()
                detail_dict["invoice_id"] = invoice_model.id_key
                detail_model = InvoiceDetailModel(**detail_dict)
                session.add(detail_model)

            session.flush()
            session.refresh(invoice_model)

            return self.schema.model_validate(invoice_model)
