from fastapi import APIRouter

from src.services.province import ProvinceService


class ProvinceController:
    """Controlador para manejar las provincias."""

    def __init__(self):
        self.router = APIRouter(tags=["Province"])
        self.service = ProvinceService()
