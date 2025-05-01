from sqlalchemy import Boolean, Column, String

from src.models.base import BaseModel


class ProductCategoryModel(BaseModel):
    __tablename__ = "product_category"

    name = Column(String, nullable=False)
    description = Column(String)
    active = Column(Boolean, nullable=False)
