from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class PromotionInventoryItemDetailModel(BaseModel):
    __tablename__ = "promotion_inventory_item_detail"

    quantity = Column(Integer, nullable=False)

    promotion_id = Column(
        Integer,
        ForeignKey("promotion.id_key", ondelete="CASCADE"),
        nullable=False,
    )
    promotion = relationship("PromotionModel", back_populates="inventory_item_details")

    inventory_item_id = Column(
        Integer,
        ForeignKey("inventory_item.id_key", ondelete="CASCADE"),
        nullable=False,
    )
    inventory_item = relationship("InventoryItemModel")
