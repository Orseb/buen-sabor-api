from datetime import datetime
from typing import List, Optional

from src.models.invoice import InvoiceType
from src.schemas.base import BaseSchema
from src.schemas.invoice_detail import ResponseInvoiceDetailSchema
from src.schemas.order import ResponseOrderSchema


class BaseInvoiceSchema(BaseSchema):
    number: str
    date: Optional[datetime] = None
    total: float
    type: InvoiceType = InvoiceType.factura
    pdf_url: Optional[str] = None


class CreateInvoiceSchema(BaseInvoiceSchema):
    order_id: int


class ResponseInvoiceSchema(BaseInvoiceSchema):
    order: ResponseOrderSchema
    details: List[ResponseInvoiceDetailSchema] = []
    id_key: int
