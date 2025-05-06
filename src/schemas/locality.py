from src.schemas.base import BaseSchema
from src.schemas.province import ResponseProvinceSchema


class BaseLocalitySchema(BaseSchema):
    name: str


class CreateLocalitySchema(BaseLocalitySchema):
    province_id: int


class ResponseLocalitySchema(BaseLocalitySchema):
    province: ResponseProvinceSchema
    id_key: int
