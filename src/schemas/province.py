from src.schemas.base import BaseSchema
from src.schemas.locality import ResponseLocalitySchema


class BaseProvinceSchema(BaseSchema):
    name: str


class CreateProvinceSchema(BaseProvinceSchema):
    country_id: int


class ResponseProvinceSchema(CreateProvinceSchema):
    localities: list[ResponseLocalitySchema] = []
    id_key: int
