from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class LocalityModel(BaseModel):
    __tablename__ = "locality"

    name = Column(String, nullable=False, unique=True)

    province_id = Column(
        Integer,
        ForeignKey("province.id_key", ondelete="CASCADE"),
        nullable=False,
    )
    province = relationship("ProvinceModel", back_populates="localities")
