from src.schemas.base import BaseSchema
from src.schemas.locality import ResponseLocalitySchema
from src.schemas.user import ResponseUserSchema


class BaseAddressSchema(BaseSchema):
    street: str
    street_number: int
    zip_code: str


class CreateAddressSchema(BaseAddressSchema):
    locality_id: int
    user_id: int


class ResponseAddressSchema(BaseSchema):
    locality: ResponseLocalitySchema
    user: ResponseUserSchema
    id_key: int
