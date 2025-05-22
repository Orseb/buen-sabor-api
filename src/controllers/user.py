from typing import List

from fastapi import Depends

from src.controllers.base_implementation import BaseControllerImplementation
from src.models.user import UserRole
from src.schemas.user import CreateUserSchema, ResponseUserSchema
from src.services.user import UserService
from src.utils.rbac import has_role


class UserController(BaseControllerImplementation):
    def __init__(self):
        super().__init__(
            create_schema=CreateUserSchema,
            response_schema=ResponseUserSchema,
            service=UserService(),
            tags=["User"],
        )

        @self.router.get("/employees/all", response_model=List[ResponseUserSchema])
        async def get_employees(
            current_user: dict = Depends(has_role([UserRole.administrador])),
        ):
            """Get all employees (users with non-client roles)."""
            return self.service.get_employees()
