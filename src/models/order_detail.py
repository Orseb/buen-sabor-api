from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class OrderDetailModel(BaseModel):
    __tablename__ = "order_detail"

    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    order_id = Column(
        Integer,
        ForeignKey("order.id_key", ondelete="CASCADE"),
        nullable=False,
    )
    order = relationship("OrderModel", back_populates="details")

    manufactured_item_id = Column(
        Integer,
        ForeignKey("manufactured_item.id_key", ondelete="CASCADE"),
        nullable=False,
    )
    manufactured_item = relationship(
        "ManufacturedItemModel", back_populates="order_details"
    )
