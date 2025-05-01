from src.controllers.base_implementation import BaseControllerImplementation
from src.schemas.user import CreateUserSchema, ResponseUserSchema
from src.services.user import UserService


class UserController(BaseControllerImplementation):
    def __init__(self):
        super().__init__(
            create_schema=CreateUserSchema,
            response_schema=ResponseUserSchema,
            service=UserService(),
            tags=["User"],
        )
