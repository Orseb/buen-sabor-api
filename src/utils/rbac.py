from typing import Any, Dict, List, Optional, Union

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from src.config.settings import settings
from src.models.user import UserRole

security = HTTPBearer()


def validate_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Dict[str, Any]:
    """Validate a JWT token and return the decoded payload."""
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(
    payload: Dict[str, Any] = Depends(validate_token),
) -> Dict[str, Any]:
    """Extract the current user from the JWT token payload."""
    try:
        user_id = int(payload.get("sub"))
        user_email = payload.get("email")
        user_role = payload.get("role")
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user_id is None or user_email is None or user_role is None:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"id": user_id, "email": user_email, "role": user_role}


def has_role(allowed_roles: Union[List[UserRole], UserRole]):
    """Dependency that checks if the current user has one of the allowed roles."""
    if isinstance(allowed_roles, UserRole):
        allowed_roles = [allowed_roles]

    async def role_checker(
        current_user: Dict[str, Any] = Depends(get_current_user),
    ) -> Dict[str, Any]:
        user_role = current_user.get("role")

        if user_role not in [role.value for role in allowed_roles]:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail=f"Not enough permissions. "
                f"Required roles: {[role.value for role in allowed_roles]}",
            )

        return current_user

    return role_checker


def optional_auth(request: Request) -> Optional[Dict[str, Any]]:
    """Optional authentication"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.replace("Bearer ", "")
    try:
        payload = jwt.decode(
            token, settings.secret_key or "", algorithms=[settings.algorithm or "HS256"]
        )
        return {
            "id": int(payload.get("sub", 0)),
            "email": payload.get("email"),
            "role": payload.get("role"),
        }
    except (JWTError, ValueError):
        return None
