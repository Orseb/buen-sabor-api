from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración de la aplicación utilizando Pydantic Settings"""

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
    frontend_url: Optional[str] = "http://localhost:5173"

    # Cloudinary
    cloudinary_api_key: Optional[str] = None

    # Email
    smtp_host: Optional[str] = "localhost"
    smtp_port: Optional[int] = 1025
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_use_tls: Optional[bool] = False
    from_email: Optional[str] = "noreply@elbuensabor.com"

    # Misc
    cash_discount: Optional[float] = 0.1

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
