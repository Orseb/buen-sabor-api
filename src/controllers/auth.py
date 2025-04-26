import logging

from authlib.integrations.base_client import OAuthError
from fastapi import APIRouter, Depends, HTTPException, Request
from starlette.status import HTTP_401_UNAUTHORIZED

from src.config.auth import oauth
from src.config.settings import settings
from src.schemas.auth import GoogleUser
from src.services.user import UserService

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Auth"])


def get_user_service() -> UserService:
    return UserService()


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
    try:

        google_user = GoogleUser(**user_response["userinfo"])

        existing_user = await user_service.get_user_by_google_sub(google_user.sub)
        print(existing_user)

        return user_response
    except Exception as e:
        logger.error("Error during Google authentication: %s", e, exc_info=True)
