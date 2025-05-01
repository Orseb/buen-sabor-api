from typing import Optional

from pydantic import EmailStr

from src.models.user import UserRole
from src.schemas.base import BaseSchema


class UserSchema(BaseSchema):
    full_name: str
    phone_number: Optional[str] = None
    email: EmailStr
    password: Optional[str] = None
    role: UserRole = "cliente"
    google_sub: Optional[str] = None
    active: Optional[bool] = True

    # TODO Optimize schema
