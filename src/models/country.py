from sqlalchemy import Column, String

from src.models.base import BaseModel


class CountryModel(BaseModel):
    __tablename__ = "country"

    name = Column(String, nullable=False)
