from typing import List

from src.schemas.base import BaseSchema
from src.schemas.locality import ResponseLocalitySchema


class BaseAddressSchema(BaseSchema):
    street: str
    street_number: int
    zip_code: str
    name: str


class CreateAddressSchema(BaseAddressSchema):
    locality_id: int
    user_id: int


class UpdateAddressSchema(BaseAddressSchema):
    locality_id: int


class ResponseAddressSchema(BaseAddressSchema):
    locality: ResponseLocalitySchema
    id_key: int
    user_id: int


class UserAddressesResponseSchema(BaseSchema):
    addresses: List[ResponseAddressSchema]
