from src.controllers.base_implementation import BaseControllerImplementation
from src.schemas.user import UserSchema
from src.services.user import UserService


class UserController(BaseControllerImplementation):
    def __init__(self):
        super().__init__(UserSchema, UserService())
