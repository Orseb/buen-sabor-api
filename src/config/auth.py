from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

from src.config.settings import settings

oauth = OAuth(
    Config(
        environ={
            "GOOGLE_CLIENT_ID": settings.google_client_id,
            "GOOGLE_CLIENT_SECRET": settings.google_client_secret,
        }
    )
)

oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)
