import enum

from sqlalchemy import Boolean, Column, Enum, String
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class UserRole(enum.Enum):
    cliente = "cliente"
    administrador = "administrador"
    cajero = "cajero"
    cocinero = "cocinero"
    delivery = "delivery"


class UserModel(BaseModel):
    __tablename__ = "user"

    full_name = Column(String, nullable=False)
    phone_number = Column(String)
    email = Column(String, nullable=False, unique=True)
    password = Column(String)
    role = Column(Enum(UserRole), nullable=False)
    google_sub = Column(String)
    active = Column(Boolean, nullable=False)
    address = relationship("AddressModel", back_populates="user")
    orders = relationship("OrderModel", back_populates="user")
