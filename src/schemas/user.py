import re
from typing import List, Optional

import bcrypt
from pydantic import EmailStr, field_validator

from src.models.user import UserRole
from src.schemas.address import ResponseAddressSchema
from src.schemas.base import BaseSchema


class BaseUserSchema(BaseSchema):
    """Base schema for user data."""

    full_name: str
    email: EmailStr


class CreateUserSchema(BaseUserSchema):
    """Schema for creating users."""

    role: Optional[UserRole] = UserRole.cliente
    phone_number: Optional[str] = None
    password: Optional[str] = None
    google_sub: Optional[str] = None
    active: Optional[bool] = True

    @field_validator("password")
    def hash_password(cls, value: Optional[str]) -> Optional[str]:
        """Hash the password using bcrypt if it's not already hashed."""
        if not value or re.compile(r"^\$2[aby]\$.{56}$").match(value):
            return value
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(value.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")


class ResponseUserSchema(CreateUserSchema):
    """Schema for user responses."""

    id_key: int
    addresses: Optional[List[ResponseAddressSchema]] = []
