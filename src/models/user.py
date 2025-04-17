from sqlalchemy import Boolean, Column, String

from src.models.base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "user"

    full_name = Column(String)
    phone_number = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    active = Column(Boolean)
