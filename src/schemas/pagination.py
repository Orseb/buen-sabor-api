from typing import Generic, List, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponseSchema(BaseModel, Generic[T]):
    total: int
    offset: int
    limit: int
    items: List[T]
