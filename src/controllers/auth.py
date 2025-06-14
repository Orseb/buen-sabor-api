from typing import Any, Dict

from authlib.integrations.base_client import OAuthError
from fastapi import APIRouter, HTTPException, Request
from starlette.responses import RedirectResponse
from starlette.status import HTTP_401_UNAUTHORIZED

from src.config.auth import oauth
from src.config.settings import settings
from src.schemas.auth import GoogleUser, LoginRequest, RegisterRequest
from src.schemas.user import ResponseUserSchema
from src.services.user import UserService
from src.utils.auth import authenticate_user, create_access_token


class AuthController:
    """Controlador para manejar la autenticación de usuarios"""

    def __init__(self):
        self.router = APIRouter(tags=["Auth"])
        self.user_service = UserService()

        @self.router.post("/register", response_model=ResponseUserSchema)
        async def register(new_user: RegisterRequest) -> ResponseUserSchema:
            """Registra un nuevo usuario en el sistema"""
            return self.user_service.save(new_user)

        @self.router.post("/login")
        async def login(user: LoginRequest) -> Dict[str, str | bool]:
            """Inicia sesión de un usuario y devuelve un token de acceso"""
            authenticated_user = authenticate_user(
                user.email, user.password, self.user_service
            )
            if not authenticated_user:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Correo o contraseña inválidos.",
                )

            return {
                "access_token": create_access_token(
                    authenticated_user.email,
                    authenticated_user.id_key,
                    authenticated_user.role,
                ),
                "first_login": authenticated_user.first_login,
            }

        @self.router.get("/google/login")
        async def google_login(request: Request) -> Dict[str, Any]:
            """Redirige al usuario a la página de inicio de sesión de Google"""
            return await oauth.google.authorize_redirect(
                request, settings.google_redirect_uri
            )

        @self.router.get("/google/callback")
        async def google_auth(request: Request) -> RedirectResponse:
            """Maneja la respuesta de Google login y redirige al frontend con el token de acceso"""
            try:
                user_response = await oauth.google.authorize_access_token(request)
            except OAuthError:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials.",
                )

            google_user = GoogleUser(**user_response["userinfo"])

            user = self.user_service.get_one_by("google_sub", google_user.sub)
            if not user:
                user = self.user_service.create_or_update_user_from_google_info(
                    google_user
                )

            access_token = create_access_token(user.email, user.id_key, user.role)

            return RedirectResponse(
                f"{settings.frontend_url}?access_token={access_token}"
            )
