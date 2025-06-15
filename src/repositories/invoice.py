from datetime import datetime
from typing import Dict, List, Tuple

from sqlalchemy import func

from src.models.invoice import InvoiceModel, InvoiceType
from src.models.invoice_detail import InvoiceDetailModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.invoice import CreateInvoiceSchema, ResponseInvoiceSchema
from src.schemas.invoice_detail import CreateInvoiceDetailSchema


class InvoiceRepository(BaseRepositoryImplementation):
    """Repositorio para manejar las facturas y sus detalles."""

    def __init__(self):
        super().__init__(
            model=InvoiceModel,
            create_schema=CreateInvoiceSchema,
            response_schema=ResponseInvoiceSchema,
        )

    def save_with_details(
        self, invoice_model: InvoiceModel, details: List[CreateInvoiceDetailSchema]
    ) -> ResponseInvoiceSchema:
        """Guarda una factura junto con sus detalles en la base de datos."""
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

    def get_revenue_by_period(
        self, start_date: datetime, end_date: datetime
    ) -> Dict[str, float]:
        """Obtiene los ingresos totales y el número de facturas en un rango de fechas."""
        with self.session_scope() as session:
            revenue_results = (
                session.query(func.sum(InvoiceModel.total).label("total_revenue"))
                .filter(
                    InvoiceModel.date >= start_date if start_date else True,
                    InvoiceModel.date <= end_date if end_date else True,
                    InvoiceModel.type == InvoiceType.factura,
                )
                .first()
            )

            invoice_count_results = (
                session.query(func.count(InvoiceModel.id_key).label("invoice_count"))
                .filter(
                    InvoiceModel.date >= start_date if start_date else True,
                    InvoiceModel.date <= end_date if end_date else True,
                    InvoiceModel.type == InvoiceType.factura,
                )
                .first()
            )
            return {
                "total_revenue": revenue_results.total_revenue or 0,
                "invoice_count": invoice_count_results.invoice_count or 0,
            }

    def get_invoices_report_data(
        self, start_date: datetime, end_date: datetime
    ) -> List[Tuple[datetime, float, str]]:
        """Obtiene los detalles de las facturas en un rango de fechas para Excel."""
        with self.session_scope() as session:
            return (
                session.query(
                    InvoiceModel.date,
                    InvoiceModel.total,
                    InvoiceModel.type,
                )
                .filter(
                    InvoiceModel.date >= start_date if start_date else True,
                    InvoiceModel.date <= end_date if end_date else True,
                    InvoiceModel.type == InvoiceType.factura,
                )
                .all()
            )
