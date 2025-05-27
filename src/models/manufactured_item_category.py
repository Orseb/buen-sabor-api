from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class ManufacturedItemCategoryModel(BaseModel):
    __tablename__ = "manufactured_item_category"

    name = Column(String, nullable=False)
    description = Column(String)

    parent_id = Column(
        Integer,
        ForeignKey("manufactured_item_category.id_key", ondelete="CASCADE"),
        nullable=True,
    )

    parent = relationship(
        "ManufacturedItemCategoryModel",
        remote_side="ManufacturedItemCategoryModel.id_key",
        back_populates="subcategories",
    )

    subcategories = relationship(
        "ManufacturedItemCategoryModel",
        back_populates="parent",
        cascade="all, delete-orphan",
    )

    manufactured_items = relationship(
        "ManufacturedItemModel", back_populates="category"
    )
