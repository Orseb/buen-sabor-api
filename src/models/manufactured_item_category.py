from sqlalchemy import Boolean, Column, String

from src.models.base import BaseModel


class ManufacturedItemCategoryModel(BaseModel):
    __tablename__ = "manufactured_item_category"

    name = Column(String, nullable=False)
    description = Column(String)
    active = Column(Boolean, nullable=False)
