from src.models.measurement_unit import MeasurementUnitModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.measurement_unit import (
    CreateMeasurementUnitSchema,
    ResponseMeasurementUnitSchema,
)


class MeasurementUnitRepository(BaseRepositoryImplementation):
    """Repositorio para manejo de unidades de medida."""

    def __init__(self):
        super().__init__(
            model=MeasurementUnitModel,
            create_schema=CreateMeasurementUnitSchema,
            response_schema=ResponseMeasurementUnitSchema,
        )
