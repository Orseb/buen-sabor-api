from sqlalchemy import Column, String

from src.models.base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "user"

    name = Column(String, index=True)
