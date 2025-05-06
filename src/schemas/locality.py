from src.schemas.base import BaseSchema


class BaseLocalitySchema(BaseSchema):
    name: str


class CreateLocalitySchema(BaseLocalitySchema):
    province_id: int


class ResponseLocalitySchema(CreateLocalitySchema):
    id_key: int
