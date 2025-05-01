from sqlalchemy import Boolean, Column, String

from src.models.base import BaseModel


class IngredientCategoryModel(BaseModel):
    __tablename__ = "ingredient_category"

    name = Column(String, nullable=False)
    description = Column(String)
    active = Column(Boolean, nullable=False)
