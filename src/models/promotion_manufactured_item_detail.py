from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class PromotionManufacturedItemDetailModel(BaseModel):
    __tablename__ = "promotion_manufactured_item_detail"

    quantity = Column(Integer, nullable=False)

    promotion_id = Column(
        Integer,
        ForeignKey("promotion.id_key", ondelete="CASCADE"),
        nullable=False,
    )
    promotion = relationship(
        "PromotionModel", back_populates="manufactured_item_details"
    )

    manufactured_item_id = Column(
        Integer,
        ForeignKey("manufactured_item.id_key", ondelete="CASCADE"),
        nullable=False,
    )
    manufactured_item = relationship("ManufacturedItemModel")
