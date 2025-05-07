import enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.models.base import BaseModel


class OrderStatus(enum.Enum):
    a_confirmar = "A confirmar"
    en_cocina = "En cocina"
    listo = "Listo"
    en_delivery = "En delivery"
    entregado = "Entregado"
    facturado = "Facturado"


class DeliveryMethod(enum.Enum):
    delivery = "Delivery"
    pickup = "Retiro en local"


class PaymentMethod(enum.Enum):
    cash = "Efectivo"
    mercado_pago = "Mercado Pago"


class OrderModel(BaseModel):
    __tablename__ = "order"

    date = Column(DateTime, server_default=func.now(), nullable=False)
    total = Column(Float, nullable=False)
    discount = Column(Float, default=0.0)
    final_total = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.a_confirmar)
    estimated_time = Column(Integer)  # in minutes
    delivery_method = Column(Enum(DeliveryMethod), nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    payment_id = Column(String)  # For Mercado Pago payment ID
    is_paid = Column(Boolean, default=False)
    notes = Column(String)

    user_id = Column(
        Integer,
        ForeignKey("user.id_key", ondelete="CASCADE"),
        nullable=False,
    )
    user = relationship("UserModel", back_populates="orders")

    address_id = Column(
        Integer,
        ForeignKey("address.id_key", ondelete="CASCADE"),
        nullable=True,
    )
    address = relationship("AddressModel", back_populates="orders")

    details = relationship("OrderDetailModel", back_populates="order")
    invoice = relationship("InvoiceModel", back_populates="order", uselist=False)
