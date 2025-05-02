from sqlalchemy import Boolean, Column, String

from src.models.base import BaseModel


class InventoryItemCategoryModel(BaseModel):
    __tablename__ = "inventory_item_category"

    name = Column(String, nullable=False)
    description = Column(String)
    active = Column(Boolean, nullable=False)
