import re
from typing import Annotated, List, Optional

import bcrypt
from pydantic import AfterValidator, EmailStr

from src.models.user import UserRole
from src.schemas.address import ResponseAddressSchema
from src.schemas.base import BaseSchema


def hash_password(value: str) -> str:
    """
    Hashes password using bcrypt
    """
    if not value or re.compile(r"^\$2[aby]\$.{56}$").match(value):
        return value
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(value.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


class BaseUserSchema(BaseSchema):
    full_name: str
    email: EmailStr


class CreateUserSchema(BaseUserSchema):
    role: Optional[UserRole] = "cliente"
    phone_number: Optional[str] = None
    password: Optional[Annotated[str, AfterValidator(hash_password)]] = None
    google_sub: Optional[str] = None
    active: Optional[bool] = True


class ResponseUserSchema(CreateUserSchema):
    id_key: int
    addresses: Optional[List[ResponseAddressSchema]] = []
