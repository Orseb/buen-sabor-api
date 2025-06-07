import enum

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.models.base import BaseModel


class InvoiceType(enum.Enum):
    factura = "factura"
    nota_credito = "nota_credito"


class InvoiceModel(BaseModel):
    __tablename__ = "invoice"

    number = Column(String, nullable=False, unique=True)
    date = Column(DateTime, server_default=func.now(), nullable=False)
    total = Column(Float, nullable=False)
    type = Column(Enum(InvoiceType), nullable=False, default=InvoiceType.factura)
    pdf_url = Column(String)

    order_id = Column(
        Integer,
        ForeignKey("order.id_key", ondelete="CASCADE"),
        nullable=False,
    )
    order = relationship("OrderModel", back_populates="invoice")
