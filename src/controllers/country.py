from fastapi import APIRouter

from src.schemas.pagination import PaginatedResponseSchema
from src.services.country import CountryService


class CountryController:
    """Controlador para manejar las operaciones relacionadas con los países."""

    def __init__(self):
        self.router = APIRouter(tags=["Country"])
        self.service = CountryService()

        @self.router.get("/", response_model=PaginatedResponseSchema)
        async def get_all_countries() -> PaginatedResponseSchema:
            """Obtiene todos los países disponibles."""
            return self.service.get_all()
