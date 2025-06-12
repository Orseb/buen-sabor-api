from typing import Any, Dict

from authlib.integrations.base_client import OAuthError
from fastapi import APIRouter, Depends, HTTPException, Request
from starlette.responses import RedirectResponse
from starlette.status import HTTP_401_UNAUTHORIZED

from src.config.auth import oauth
from src.config.settings import settings
from src.schemas.auth import GoogleUser, LoginRequest, RegisterRequest
from src.services.user import UserService
from src.utils.auth import authenticate_user, create_access_token

router = APIRouter(tags=["Auth"])


def get_user_service() -> UserService:
    """Dependency to get the user service."""
    return UserService()


@router.post("/register")
async def register(
    new_user: RegisterRequest, user_service: UserService = Depends(get_user_service)
) -> Dict[str, Any]:
    """Register a new user."""
    created_user = user_service.save(new_user)
    return created_user.model_dump()


@router.post("/login")
async def login(
    user: LoginRequest, user_service: UserService = Depends(get_user_service)
) -> Dict[str, str | bool]:
    """Authenticate a user and return an access token."""
    authenticated_user = authenticate_user(user.email, user.password, user_service)
    if not authenticated_user or not authenticated_user.active:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Correo o contraseña inválidos."
        )

    return {
        "access_token": create_access_token(
            authenticated_user.email, authenticated_user.id_key, authenticated_user.role
        ),
        "first_login": authenticated_user.first_login,
    }


@router.get("/google/login")
async def google_login(request: Request) -> Dict[str, Any]:
    """Redirect to Google OAuth login."""
    return await oauth.google.authorize_redirect(request, settings.google_redirect_uri)


@router.get("/google/callback")
async def google_auth(
    request: Request, user_service: UserService = Depends(get_user_service)
) -> RedirectResponse:
    """Handle Google OAuth callback and authenticate the user."""
    try:
        user_response = await oauth.google.authorize_access_token(request)
    except OAuthError:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Could not validate credentials."
        )

    google_user = GoogleUser(**user_response["userinfo"])

    user = user_service.get_one_by("google_sub", google_user.sub)
    if not user:
        user = user_service.create_or_update_user_from_google_info(google_user)

    access_token = create_access_token(user.email, user.id_key, user.role)

    return RedirectResponse(f"{settings.frontend_url}?access_token={access_token}")
