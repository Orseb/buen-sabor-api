from src.schemas.base import BaseSchema


class BaseCountrySchema(BaseSchema):
    name: str


class CreateCountrySchema(BaseCountrySchema):
    pass


class ResponseCountrySchema(CreateCountrySchema):
    id_key: int
