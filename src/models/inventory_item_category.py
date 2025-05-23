from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class InventoryItemCategoryModel(BaseModel):
    __tablename__ = "inventory_item_category"

    name = Column(String, nullable=False)
    description = Column(String)
    active = Column(Boolean, nullable=False)

    parent_id = Column(
        Integer,
        ForeignKey("inventory_item_category.id_key", ondelete="CASCADE"),
        nullable=True,
    )

    parent = relationship(
        "InventoryItemCategoryModel",
        remote_side="InventoryItemCategoryModel.id_key",
        back_populates="subcategories",
    )

    subcategories = relationship(
        "InventoryItemCategoryModel",
        back_populates="parent",
        cascade="all, delete-orphan",
    )

    inventory_items = relationship("InventoryItemModel", back_populates="category")
