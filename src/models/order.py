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
from src.models.order_inventory_detail import OrderInventoryDetailModel  # noqa


class OrderStatus(enum.Enum):
    a_confirmar = "a_confirmar"
    en_cocina = "en_cocina"
    listo = "listo"
    en_delivery = "en_delivery"
    entregado = "entregado"
    facturado = "facturado"


class DeliveryMethod(enum.Enum):
    delivery = "delivery"
    pickup = "pickup"


class PaymentMethod(enum.Enum):
    cash = "cash"
    mercado_pago = "mercado_pago"


class OrderModel(BaseModel):
    __tablename__ = "order"

    date = Column(DateTime, server_default=func.now(), nullable=False)
    total = Column(Float, nullable=False)
    discount = Column(Float, default=0.0)
    final_total = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.a_confirmar)
    estimated_time = Column(Integer)
    delivery_method = Column(Enum(DeliveryMethod), nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    payment_id = Column(String)
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
    inventory_details = relationship(
        "OrderInventoryDetailModel", back_populates="order"
    )
    invoice = relationship("InvoiceModel", back_populates="order", uselist=False)
