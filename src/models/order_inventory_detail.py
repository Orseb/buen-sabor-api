from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class OrderInventoryDetailModel(BaseModel):
    __tablename__ = "order_inventory_detail"

    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    order_id = Column(
        Integer, ForeignKey("order.id_key", ondelete="CASCADE"), nullable=False
    )
    order = relationship("OrderModel", back_populates="inventory_details")

    inventory_item_id = Column(
        Integer, ForeignKey("inventory_item.id_key", ondelete="CASCADE"), nullable=False
    )
    inventory_item = relationship(
        "InventoryItemModel", back_populates="order_inventory_details"
    )
