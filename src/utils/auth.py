from datetime import UTC, datetime, timedelta

import bcrypt
from jose import jwt
from pydantic import EmailStr

from src.config.settings import settings
from src.models.user import UserRole
from src.repositories.user import UserRepository
from src.schemas.user import UserSchema


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


def hash_password(password: str) -> str:
    """
    Hashes password using bcrypt
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def authenticate_user(user_email: EmailStr, user_password: str) -> UserSchema | None:
    existing_user = UserRepository().get_user_by_email(user_email)
    if not existing_user:
        return None

    matching_passwords = bcrypt.checkpw(
        user_password.encode("utf-8"), existing_user.password.encode("utf-8")
    )
    if not matching_passwords:
        return None

    return existing_user
