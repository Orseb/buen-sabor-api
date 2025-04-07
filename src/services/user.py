from src.models.user import UserModel
from src.repositories.user import UserRepository
from src.schemas.user import UserSchema
from src.services.base_implementation import BaseServiceImplementation


class UserService(BaseServiceImplementation):

    def __init__(self):
        super().__init__(
            repository=UserRepository(), model=UserModel, schema=UserSchema
        )
