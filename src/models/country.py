from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class CountryModel(BaseModel):
    __tablename__ = "country"

    name = Column(String, nullable=False)

    provinces = relationship("ProvinceModel", back_populates="country")
