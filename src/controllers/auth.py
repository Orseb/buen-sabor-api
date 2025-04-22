from authlib.integrations.base_client import OAuthError
from fastapi import APIRouter, HTTPException, Request
from starlette.status import HTTP_401_UNAUTHORIZED

from src.config.auth import oauth
from src.config.settings import settings

router = APIRouter(tags=["Auth"])


@router.get("/google/login")
async def google_login(request: Request):
    return await oauth.google.authorize_redirect(request, settings.google_redirect_uri)


@router.get("/google/callback")
async def google_auth(request: Request):
    try:
        user_response = await oauth.google.authorize_access_token(request)
    except OAuthError:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Could not validate credentials."
        )

    return user_response
