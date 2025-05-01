from authlib.integrations.base_client import OAuthError
from fastapi import APIRouter, Depends, HTTPException, Request
from psycopg2.errors import UniqueViolation  # noqa
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_401_UNAUTHORIZED

from src.config.auth import oauth
from src.config.settings import settings
from src.schemas.auth import GoogleUser, LoginRequest, RegisterRequest
from src.services.user import UserService
from src.utils.auth import authenticate_user, create_access_token

router = APIRouter(tags=["Auth"])


def get_user_service() -> UserService:
    return UserService()


@router.post("/register")
async def register(
    new_user: RegisterRequest, user_service: UserService = Depends(get_user_service)
):
    try:
        new_user = user_service.save(new_user)

    except IntegrityError as error:
        if isinstance(error.orig, UniqueViolation):
            raise HTTPException(
                status_code=400, detail="Ya existe un usuario con ese correo."
            )

    return new_user


@router.post("/login")
async def login(user: LoginRequest):
    user = authenticate_user(user.email, user.password)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Correo o contraseña inválidos."
        )

    return {"access_token": create_access_token(user.email, user.id_key, user.role)}


@router.get("/google/login")
async def google_login(request: Request):
    return await oauth.google.authorize_redirect(request, settings.google_redirect_uri)


@router.get("/google/callback")
async def google_auth(
    request: Request, user_service: UserService = Depends(get_user_service)
):
    try:
        user_response = await oauth.google.authorize_access_token(request)
    except OAuthError:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Could not validate credentials."
        )

    google_user = GoogleUser(**user_response["userinfo"])

    user = await user_service.get_user_by_google_sub(google_user.sub)
    if not user:
        user = await user_service.create_or_update_user_from_google_info(google_user)

    return {"access_token": create_access_token(user.email, user.id_key, user.role)}
