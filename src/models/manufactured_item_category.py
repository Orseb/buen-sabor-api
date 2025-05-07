from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class ManufacturedItemCategoryModel(BaseModel):
    __tablename__ = "manufactured_item_category"

    name = Column(String, nullable=False)
    description = Column(String)
    active = Column(Boolean, nullable=False)

    manufactured_items = relationship(
        "ManufacturedItemModel", back_populates="category"
    )
