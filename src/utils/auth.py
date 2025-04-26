from datetime import UTC, datetime, timedelta

from jose import jwt
from pydantic import EmailStr

from src.config.settings import settings
from src.models.user import UserRole


def create_access_token(user_email: EmailStr, user_id: int, user_role: UserRole) -> str:
    """
    Generates an access token based on the user email, id and role
    """
    expires_in = datetime.now(UTC) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    encoding = {
        "email": user_email,
        "sub": user_id,
        "role": user_role,
        "exp": expires_in,
    }

    return jwt.encode(encoding, settings.secret_key, algorithm=settings.algorithm)
