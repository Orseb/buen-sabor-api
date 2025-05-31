from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from fastapi import APIRouter, Depends

from src.controllers.base import BaseController
from src.models.user import UserRole
from src.schemas.base import BaseSchema
from src.schemas.pagination import PaginatedResponseSchema
from src.services.base import BaseService
from src.utils.rbac import has_role

S = TypeVar("S", bound=BaseSchema)
C = TypeVar("C", bound=BaseSchema)


class BaseControllerImplementation(Generic[S, C], BaseController[S]):
    """Generic implementation of the BaseController interface."""

    def __init__(
        self,
        create_schema: Type[C],
        response_schema: Type[S],
        service: BaseService,
        tags: Optional[List[str]] = None,
        required_roles: Optional[List[UserRole]] = None,
    ):
        """Initialize the controller with service and schema types."""
        self._service = service
        self.create_schema = create_schema
        self.response_schema = response_schema
        self.router = APIRouter(tags=tags or [])

        if required_roles is None:
            required_roles = [UserRole.administrador]

        role_dependency = has_role(required_roles)

        self._register_routes(role_dependency)

    def _register_routes(self, role_dependency: Any) -> None:
        """Register standard CRUD routes with the router."""

        from src.utils.rbac import get_current_user

        @self.router.get("/", response_model=PaginatedResponseSchema)
        async def get_all(
            offset: int = 0,
            limit: int = 10,
            current_user: Dict[str, Any] = Depends(get_current_user),
        ):
            return self.get_all(offset, limit)

        @self.router.get("/{id_key}", response_model=self.response_schema)
        async def get_one(
            id_key: int, current_user: Dict[str, Any] = Depends(get_current_user)
        ):
            return self.get_one(id_key)

        @self.router.post("/", response_model=self.response_schema)
        async def save(
            schema_in: self.create_schema,
            current_user: Dict[str, Any] = Depends(role_dependency),
        ):
            return self.save(schema_in)

        @self.router.put("/{id_key}", response_model=self.response_schema)
        async def update(
            id_key: int,
            schema_in: self.create_schema,
            current_user: Dict[str, Any] = Depends(role_dependency),
        ):
            return self.update(id_key, schema_in)

        @self.router.delete("/{id_key}")
        async def delete(
            id_key: int, current_user: Dict[str, Any] = Depends(role_dependency)
        ):
            return self.delete(id_key)

    @property
    def service(self) -> BaseService:
        """Get the service for business logic."""
        return self._service

    @property
    def schema(self) -> Type[S]:
        """Get the Pydantic schema class for responses."""
        return self.response_schema

    def get_all(self, offset: int = 0, limit: int = 10) -> PaginatedResponseSchema:
        """Get all records paginated."""
        return self.service.get_all(offset, limit)

    def get_one(self, id_key: int) -> S:
        """Get a record by primary key."""
        return self.service.get_one(id_key)

    def save(self, schema: C) -> S:
        """Save a new record."""
        return self.service.save(schema)

    def update(self, id_key: int, schema: C) -> S:
        """Update an existing record."""
        return self.service.update(id_key, schema)

    def delete(self, id_key: int) -> S:
        """Delete a record by primary key."""
        return self.service.delete(id_key)

    @schema.setter
    def schema(self, value: Type[S]) -> None:
        self.response_schema = value

    @service.setter
    def service(self, value: BaseService) -> None:
        self._service = value
