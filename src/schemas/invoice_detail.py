from typing import Optional

from src.schemas.base import BaseSchema


class BaseInvoiceDetailSchema(BaseSchema):
    item_name: str
    quantity: int
    unit_price: float
    subtotal: float
    item_type: str


class CreateInvoiceDetailSchema(BaseInvoiceDetailSchema):
    invoice_id: Optional[int] = None
    manufactured_item_id: Optional[int] = None
    inventory_item_id: Optional[int] = None


class ResponseInvoiceDetailSchema(BaseInvoiceDetailSchema):
    id_key: int
    invoice_id: int
    manufactured_item_id: Optional[int] = None
    inventory_item_id: Optional[int] = None
