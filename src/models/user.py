import enum

from sqlalchemy import Boolean, Column, Enum, String

from src.models.base import BaseModel


class UserRole(enum.Enum):
    cliente = "cliente"
    administrador = "administrador"
    cajero = "cajero"
    cocinero = "cocinero"
    delivery = "delivery"


class UserModel(BaseModel):
    __tablename__ = "user"

    full_name = Column(String)
    phone_number = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.cliente)
    google_sub = Column(String)
    active = Column(Boolean)
