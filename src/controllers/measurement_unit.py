from fastapi import APIRouter

from src.schemas.pagination import PaginatedResponseSchema
from src.services.measurement_unit import MeasurementUnitService


class MeasurementUnitController:
    """Controlador para manejar las unidades de medida."""

    def __init__(self):
        self.router = APIRouter(tags=["Measurement Unit"])
        self.service = MeasurementUnitService()

        @self.router.get("/", response_model=PaginatedResponseSchema)
        async def get_all_measurement_units(
            offset: int = 0, limit: int = 10
        ) -> PaginatedResponseSchema:
            """Obtiene todas las unidades de medida."""
            return self.service.get_all(offset, limit)
