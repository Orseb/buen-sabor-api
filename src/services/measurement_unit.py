from src.models.measurement_unit import MeasurementUnitModel
from src.repositories.measurement_unit import MeasurementUnitRepository
from src.schemas.measurement_unit import (
    CreateMeasurementUnitSchema,
    ResponseMeasurementUnitSchema,
)
from src.services.base_implementation import BaseServiceImplementation


class MeasurementUnitService(BaseServiceImplementation):

    def __init__(self):
        super().__init__(
            repository=MeasurementUnitRepository(),
            model=MeasurementUnitModel,
            create_schema=CreateMeasurementUnitSchema,
            response_schema=ResponseMeasurementUnitSchema,
        )
