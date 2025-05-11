import mercadopago

from src.config.settings import settings

sdk = mercadopago.SDK(settings.prod_access_token)
