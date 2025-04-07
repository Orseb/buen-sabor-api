from src.models.user import UserModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.user import UserSchema


class UserRepository(BaseRepositoryImplementation):
    def __init__(self):
        super().__init__(UserModel, UserSchema)
