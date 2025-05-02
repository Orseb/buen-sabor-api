from src.controllers.base_implementation import BaseControllerImplementation
from src.schemas.measurement_unit import (
    CreateMeasurementUnitSchema,
    ResponseMeasurementUnitSchema,
)
from src.services.measurement_unit import MeasurementUnitService


class MeasurementUnitController(BaseControllerImplementation):
    def __init__(self):
        super().__init__(
            create_schema=CreateMeasurementUnitSchema,
            response_schema=ResponseMeasurementUnitSchema,
            service=MeasurementUnitService(),
            tags=["Measurement Unit"],
        )
