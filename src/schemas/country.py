from src.schemas.base import BaseSchema
from src.schemas.province import ResponseProvinceSchema


class BaseCountrySchema(BaseSchema):
    name: str


class CreateCountrySchema(BaseCountrySchema):
    pass


class ResponseCountrySchema(CreateCountrySchema):
    provinces: list[ResponseProvinceSchema] = []
    id_key: int
