from typing import Any, Dict, List

from fastapi import Depends, HTTPException

from src.controllers.base_implementation import BaseControllerImplementation
from src.models.user import UserRole
from src.repositories.base_implementation import RecordNotFoundError
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

        @self.router.get("/employees/all", response_model=List[ResponseUserSchema])
        async def get_employees(
            current_user: dict = Depends(has_role([UserRole.administrador])),
        ):
            """Get all employees (users with non-client roles)."""
            return self.service.get_employees()

        @self.router.get("/clients/all", response_model=List[ResponseUserSchema])
        async def get_clients(
            current_user: dict = Depends(has_role([UserRole.administrador])),
        ):
            """Get all clients (users with client roles)."""
            return self.service.get_clients()

        @self.router.put("/{id_key}/image", response_model=ResponseUserSchema)
        def update_user_image(
            id_key: int,
            image_base64: str,
            current_user: Dict[str, Any] = Depends(get_current_user),
        ):
            try:
                return self.service.update_image(id_key, image_base64)
            except RecordNotFoundError as error:
                raise HTTPException(status_code=404, detail=str(error))
