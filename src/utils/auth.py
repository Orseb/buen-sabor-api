from datetime import UTC, datetime, timedelta
from typing import Optional

import bcrypt
from jose import jwt
from pydantic import EmailStr

from src.config.settings import settings
from src.models.user import UserRole
from src.schemas.user import ResponseUserSchema
from src.services.user import UserService


def create_access_token(user_email: EmailStr, user_id: int, user_role: UserRole) -> str:
    """Genera un token de acceso JWT para un usuario."""
    expires_in = datetime.now(UTC) + timedelta(
        minutes=int(settings.access_token_expire_minutes or 30)
    )

    encoding = {
        "email": user_email,
        "sub": str(user_id),
        "role": user_role,
        "exp": expires_in,
    }

    return jwt.encode(
        encoding, settings.secret_key or "", algorithm=settings.algorithm or "HS256"
    )


def authenticate_user(
    user_email: EmailStr, user_password: str, user_service: UserService
) -> Optional[ResponseUserSchema]:
    """Autentica a un usuario verificando su email y contraseña."""
    existing_user = user_service.get_one_by("email", user_email)

    if not existing_user or not existing_user.password:
        return None

    if not bcrypt.checkpw(
        user_password.encode("utf-8"), existing_user.password.encode("utf-8")
    ):
        return None

    return existing_user


def hash_password(password: str) -> str:
    """Hashea una contraseña usando bcrypt."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña en texto plano coincide con un hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )
