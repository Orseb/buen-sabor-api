from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class ProvinceModel(BaseModel):
    __tablename__ = "province"

    name = Column(String, nullable=False, unique=True)

    country_id = Column(
        Integer,
        ForeignKey("country.id_key", ondelete="CASCADE"),
        nullable=False,
    )
    country = relationship("CountryModel", back_populates="provinces")
