from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class ManufacturedItemDetailModel(BaseModel):
    __tablename__ = "manufactured_item_detail"

    quantity = Column(Float, nullable=False)

    manufactured_item_id = Column(
        Integer,
        ForeignKey("manufactured_item.id_key", ondelete="CASCADE"),
        nullable=False,
    )
    manufactured_item = relationship("ManufacturedItemModel", back_populates="details")

    inventory_item_id = Column(
        Integer,
        ForeignKey("inventory_item.id_key", ondelete="CASCADE"),
        nullable=False,
    )
    inventory_item = relationship(
        "InventoryItemModel", back_populates="manufactured_item_details"
    )
