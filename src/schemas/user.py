from typing import Optional

from src.schemas.base import BaseSchema


class UserSchema(BaseSchema):
    name: Optional[str] = None
