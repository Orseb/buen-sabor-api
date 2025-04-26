from typing import Optional

from pydantic import EmailStr

from src.models.user import UserRole
from src.schemas.base import BaseSchema


class UserSchema(BaseSchema):
    full_name: str
    phone_number: Optional[str]
    email: EmailStr
    password: Optional[str]
    role: UserRole = "cliente"
    google_sub: str
    active: Optional[bool] = True
