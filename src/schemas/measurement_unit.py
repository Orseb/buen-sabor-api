from src.schemas.base import BaseSchema


class BaseMeasurementUnitSchema(BaseSchema):
    name: str
    active: bool = True


class CreateMeasurementUnitSchema(BaseMeasurementUnitSchema):
    pass


class ResponseMeasurementUnitSchema(CreateMeasurementUnitSchema):
    id_key: int
