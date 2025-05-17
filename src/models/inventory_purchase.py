from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.models.base import BaseModel


class InventoryPurchaseModel(BaseModel):
    __tablename__ = "inventory_purchase"

    inventory_item_id = Column(
        Integer,
        ForeignKey("inventory_item.id_key", ondelete="CASCADE"),
        nullable=False,
    )
    inventory_item = relationship("InventoryItemModel", back_populates="purchases")

    quantity = Column(Integer, nullable=False)
    purchase_date = Column(DateTime, server_default=func.now(), nullable=False)
    unit_cost = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)
    notes = Column(String, nullable=True)
