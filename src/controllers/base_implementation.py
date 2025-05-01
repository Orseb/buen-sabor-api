from typing import List, Optional, Type

from fastapi import APIRouter, HTTPException
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

from src.controllers.base import BaseController
from src.repositories.base_implementation import RecordNotFoundError
from src.schemas.base import BaseSchema
from src.services.base import BaseService


class BaseControllerImplementation(BaseController):
    """Base controller implementation."""

    def __init__(
        self,
        create_schema: Type[BaseSchema],
        response_schema: Type[BaseSchema],
        service: BaseService,
        tags: Optional[List[str]] = None,
    ):
        self.service = service
        self.create_schema = create_schema
        self.response_schema = response_schema
        self.router = APIRouter(tags=tags)

        @self.router.get("/", response_model=List[response_schema])
        async def get_all():
            return self.get_all()

        @self.router.get("/{id_key}", response_model=response_schema)
        async def get_one(id_key: int):
            try:
                return self.get_one(id_key)
            except RecordNotFoundError as error:
                raise HTTPException(status_code=404, detail=str(error))

        @self.router.post("/", response_model=response_schema)
        async def save(schema_in: create_schema):
            try:
                return self.save(schema_in)
            except IntegrityError as error:
                if isinstance(error.orig, UniqueViolation):
                    raise HTTPException(
                        status_code=400, detail="Unique constraint violated."
                    )
                raise HTTPException(
                    status_code=500, detail="An unexpected database error occurred."
                )

        @self.router.put("/{id_key}", response_model=response_schema)
        async def update(id_key: int, schema_in: create_schema):
            try:
                return self.update(id_key, schema_in)
            except RecordNotFoundError as error:
                raise HTTPException(status_code=404, detail=str(error))
            except IntegrityError as error:
                if isinstance(error.orig, UniqueViolation):
                    raise HTTPException(
                        status_code=400, detail="Unique constraint violated."
                    )
                raise HTTPException(
                    status_code=500, detail="An unexpected database error occurred."
                )

        @self.router.delete("/{id_key}")
        async def delete(id_key: int):
            try:
                return self.delete(id_key)
            except RecordNotFoundError as error:
                raise HTTPException(status_code=404, detail=str(error))

    @property
    def service(self) -> BaseService:
        """Service to access database."""
        return self._service

    @property
    def schema(self) -> Type[BaseSchema]:
        """Pydantic Schema to validate data."""
        return self.response_schema

    def get_all(self) -> List[BaseSchema]:
        """Get all data."""
        return self.service.get_all()

    def get_one(self, id_key: int) -> BaseSchema:
        """Get one data."""
        return self.service.get_one(id_key)

    def save(self, schema: BaseSchema) -> BaseSchema:
        """Save data."""
        return self.service.save(schema)

    def update(self, id_key: int, schema: BaseSchema) -> BaseSchema:
        """Update data."""
        return self.service.update(id_key, schema)

    def delete(self, id_key: int) -> BaseSchema:
        """Delete data."""
        return self.service.delete(id_key)

    @schema.setter
    def schema(self, value):
        self.response_schema = value

    @service.setter
    def service(self, value):
        self._service = value
