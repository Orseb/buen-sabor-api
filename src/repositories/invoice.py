from datetime import datetime
from typing import Dict, List, Tuple

from sqlalchemy import and_, func, select

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
            stmt = select(
                func.coalesce(func.sum(InvoiceModel.total), 0).label("total_revenue"),
                func.count(InvoiceModel.id_key).label("invoice_count"),
            ).where(
                and_(
                    self._build_invoice_date_filter(start_date, end_date),
                    InvoiceModel.type == InvoiceType.factura,
                )
            )

            result = session.execute(stmt).first()
            return {
                "total_revenue": result.total_revenue,
                "invoice_count": result.invoice_count,
            }

    def get_invoices_report_data(
        self, start_date: datetime, end_date: datetime
    ) -> List[Tuple[datetime, float, str]]:
        """Obtiene los detalles de las facturas en un rango de fechas para Excel."""
        with self.session_scope() as session:
            stmt = (
                select(InvoiceModel.date, InvoiceModel.total, InvoiceModel.type)
                .where(
                    and_(
                        self._build_invoice_date_filter(start_date, end_date),
                        InvoiceModel.type == InvoiceType.factura,
                    )
                )
                .order_by(InvoiceModel.date.desc())
            )

            result = session.execute(stmt)
            return result.all()

    def _build_invoice_date_filter(self, start_date: datetime, end_date: datetime):
        """Construye un filtro para las fechas de las facturas."""
        conditions = []
        if start_date:
            conditions.append(InvoiceModel.date >= start_date)
        if end_date:
            conditions.append(InvoiceModel.date <= end_date)

        return and_(*conditions) if conditions else True

    def search_invoices_by_number(
        self, search_term: str, offset: int, limit: int
    ) -> List[ResponseInvoiceSchema]:
        """Busca facturas activas por número."""
        with self.session_scope() as session:
            stmt = (
                select(self.model)
                .where(
                    self.model.number.ilike(f"%{search_term}%"),
                    self.model.active.is_(True),
                )
                .offset(offset)
                .limit(limit)
            )

            result = session.execute(stmt)
            return [self.schema.model_validate(row) for row in result.scalars()]

    def count_search_invoices_by_number(self, search_term: str) -> int:
        """Cuenta facturas activas que coinciden con el término de búsqueda por número."""
        with self.session_scope() as session:
            stmt = select(func.count()).where(
                self.model.number.ilike(f"%{search_term}%"),
                self.model.active.is_(True),
            )
            return session.scalar(stmt)
