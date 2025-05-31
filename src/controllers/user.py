from typing import Any, Dict

from fastapi import Depends

from src.controllers.base_implementation import BaseControllerImplementation
from src.models.user import UserRole
from src.schemas.pagination import PaginatedResponseSchema
from src.schemas.user import CreateUserSchema, ResponseUserSchema
from src.services.user import UserService
from src.utils.rbac import get_current_user, has_role


class UserController(BaseControllerImplementation):
    def __init__(self):
        super().__init__(
            create_schema=CreateUserSchema,
            response_schema=ResponseUserSchema,
            service=UserService(),
            tags=["User"],
        )

        @self.router.get("/employees/all", response_model=PaginatedResponseSchema)
        async def get_employees(
            offset: int = 0,
            limit: int = 10,
            current_user: dict = Depends(has_role([UserRole.administrador])),
        ):
            """Get all employees (users with non-client roles)."""
            return self.service.get_employees(offset, limit)

        @self.router.get("/clients/all", response_model=PaginatedResponseSchema)
        async def get_clients(
            offset: int = 0,
            limit: int = 10,
            current_user: dict = Depends(has_role([UserRole.administrador])),
        ):
            """Get all clients (users with client roles)."""
            return self.service.get_clients(offset, limit)

        @self.router.put("/update/token", response_model=self.response_schema)
        async def update(
            schema_in: self.create_schema,
            current_user: Dict[str, Any] = Depends(get_current_user),
        ):
            return self.service.update(current_user["id"], schema_in)
