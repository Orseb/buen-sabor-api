import re
from typing import Optional

import bcrypt
from pydantic import BaseModel, EmailStr, field_validator

from src.models.user import UserRole


class RegisterRequest(BaseModel):
    """Schema for user registration requests."""

    full_name: str
    email: EmailStr
    phone_number: str
    password: str
    role: UserRole = UserRole.cliente
    active: bool = True

    @field_validator("password")
    def hash_password(cls, value: str) -> str:
        """Hash the password using bcrypt."""
        if not value or re.compile(r"^\$2[aby]\$.{56}$").match(value):
            return value
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(value.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")


class LoginRequest(BaseModel):
    """Schema for user login requests."""

    email: EmailStr
    password: str


class GoogleUser(BaseModel):
    """Schema for Google OAuth user information."""

    sub: str
    email: EmailStr
    name: str
    picture: Optional[str] = None
