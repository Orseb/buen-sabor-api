import re
from typing import Annotated

import bcrypt
from pydantic import AfterValidator, BaseModel, EmailStr

from src.models.user import UserRole


def hash_password(value: str) -> str:
    """
    Hashes password using bcrypt
    """
    if re.compile(r"^\$2[aby]\$.{56}$").match(value):
        return value
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(value.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    password: Annotated[str, AfterValidator(hash_password)]
    role: UserRole = "cliente"
    active: bool = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class GoogleUser(BaseModel):
    sub: str
    email: str
    name: str
    picture: str
