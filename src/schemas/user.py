from pydantic import EmailStr

from src.models.user import UserRole
from src.schemas.base import BaseSchema


class UserSchema(BaseSchema):
    full_name: str
    phone_number: str
    email: EmailStr
    password: str
    role: UserRole
    active: bool = True
