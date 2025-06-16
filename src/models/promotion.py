from sqlalchemy import Column, Float, String
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class PromotionModel(BaseModel):
    __tablename__ = "promotion"

    name = Column(String, nullable=False)
    description = Column(String)
    discount_percentage = Column(Float, nullable=False)

    manufactured_item_details = relationship(
        "PromotionManufacturedItemDetailModel",
        back_populates="promotion",
        cascade="all, delete-orphan",
    )

    inventory_item_details = relationship(
        "PromotionInventoryItemDetailModel",
        back_populates="promotion",
        cascade="all, delete-orphan",
    )
