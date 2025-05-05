from src.schemas.base import BaseSchema
from src.schemas.country import ResponseCountrySchema


class BaseProvinceSchema(BaseSchema):
    name: str


class CreateProvinceSchema(BaseProvinceSchema):
    country_id: int


class ResponseProvinceSchema(BaseProvinceSchema):
    country: ResponseCountrySchema
    id_key: int
