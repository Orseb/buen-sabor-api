import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    db_username: str = os.getenv("DB_USERNAME")
    db_password: str = os.getenv("DB_PASSWORD")
    db_host: str = os.getenv("DB_HOST")
    db_port: str = os.getenv("DB_PORT")
    db_name: str = os.getenv("DB_NAME")

    # JWT
    secret_key: str = os.getenv("SECRET_KEY")
    algorithm: str = os.getenv("ALGORITHM")
    access_token_expire_minutes: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

    # OAuth
    google_client_id: str = os.getenv("GOOGLE_CLIENT_ID")
    google_client_secret: str = os.getenv("GOOGLE_CLIENT_SECRET")
    google_redirect_uri: str = os.getenv("GOOGLE_REDIRECT_URI")

    # Mercado Pago
    prod_access_token: str = os.getenv("PROD_ACCESS_TOKEN")


settings = Settings()
