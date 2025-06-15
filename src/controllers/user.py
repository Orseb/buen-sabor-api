from typing import Any, Dict

from fastapi import Body, Depends, HTTPException

from src.controllers.base_implementation import BaseControllerImplementation
from src.models.user import UserRole
from src.schemas.pagination import PaginatedResponseSchema
from src.schemas.user import CreateUserSchema, ResponseUserSchema
from src.services.user import UserService
from src.utils.auth import hash_password
from src.utils.rbac import get_current_user, has_role


class UserController(BaseControllerImplementation):
    """Controlador para manejar usuarios."""

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
            _: dict = Depends(has_role([UserRole.administrador])),
        ) -> PaginatedResponseSchema:
            """Obtiene todos los empleados."""
            return self.service.get_employees(offset, limit)

        @self.router.get("/clients/all", response_model=PaginatedResponseSchema)
        async def get_clients(
            offset: int = 0,
            limit: int = 10,
            _: dict = Depends(has_role([UserRole.administrador])),
        ) -> PaginatedResponseSchema:
            """Obtiene todos los clientes."""
            return self.service.get_clients(offset, limit)

        @self.router.put("/update/token", response_model=ResponseUserSchema)
        async def update(
            schema_in: CreateUserSchema,
            current_user: Dict[str, Any] = Depends(get_current_user),
        ) -> ResponseUserSchema:
            """Actualiza la informacion de un usuario en base a su sesion."""
            return self.service.update(current_user["id"], schema_in)

        @self.router.put("/employee/password", response_model=ResponseUserSchema)
        async def update_employee_password(
            password: str = Body(..., embed=True),
            current_user: Dict[str, Any] = Depends(get_current_user),
        ) -> ResponseUserSchema:
            """Actualiza la contrasena de un empleado."""
            employee = self.service.get_one(current_user["id"])
            if not employee.first_login:
                raise HTTPException(
                    status_code=400,
                    detail="La contrasenia solo puede ser actualizada en el primer login.",
                )

            return self.service.update_employee_password(
                current_user["id"], hash_password(password)
            )
