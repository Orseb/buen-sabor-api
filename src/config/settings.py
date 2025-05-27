from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    db_username: Optional[str] = None
    db_password: Optional[str] = None
    db_host: Optional[str] = None
    db_port: Optional[str] = None
    db_name: Optional[str] = None

    # JWT
    secret_key: Optional[str] = None
    algorithm: Optional[str] = "HS256"
    access_token_expire_minutes: Optional[int] = 30

    # OAuth
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None
    google_redirect_uri: Optional[str] = None

    # Mercado Pago
    prod_access_token: Optional[str] = None

    # Frontend
    frontend_url: Optional[str] = "http://localhost:8000/docs"

    # Cloudinary
    cloudinary_api_key: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
