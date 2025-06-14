from fastapi import APIRouter

from src.services.locality import LocalityService


class LocalityController:
    """Controlador para manejar las localidades."""

    def __init__(self):
        self.router = APIRouter(tags=["Locality"])
        self.service = LocalityService()
