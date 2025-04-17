from pydantic import EmailStr

from src.schemas.base import BaseSchema


class UserSchema(BaseSchema):
    full_name: str
    phone_number: str
    email: EmailStr
    password: str
    active: bool = True
