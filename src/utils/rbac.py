from typing import Any, Dict, List, Union

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from src.config.settings import settings
from src.models.user import UserRole

security = HTTPBearer()


def validate_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Dict[str, Any]:
    """Valida el token JWT y devuelve el payload."""
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
    """Obtiene el usuario actual a partir del token JWT."""
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
    """Decorador para verificar si el usuario tiene uno de los roles permitidos."""
    if isinstance(allowed_roles, UserRole):
        allowed_roles = [allowed_roles]

    async def role_checker(
        current_user: Dict[str, Any] = Depends(get_current_user),
    ) -> Dict[str, Any]:
        """Verifica si el usuario actual tiene uno de los roles permitidos."""
        user_role = current_user.get("role")

        if user_role not in [role.value for role in allowed_roles]:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail=f"Not enough permissions. "
                f"Required roles: {[role.value for role in allowed_roles]}",
            )

        return current_user

    return role_checker
