from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class AddressModel(BaseModel):
    __tablename__ = "address"

    street = Column(String, nullable=False)
    street_number = Column(Integer, nullable=False)
    zip_code = Column(String, nullable=False)
    name = Column(String, nullable=False)

    locality_id = Column(
        Integer,
        ForeignKey("locality.id_key", ondelete="CASCADE"),
        nullable=False,
    )
    locality = relationship("LocalityModel", back_populates="addresses")

    user_id = Column(
        Integer,
        ForeignKey("user.id_key", ondelete="CASCADE"),
        nullable=False,
    )
    user = relationship("UserModel", back_populates="addresses")

    orders = relationship("OrderModel", back_populates="address")
