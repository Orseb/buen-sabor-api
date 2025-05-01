from src.models.user import UserModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.user import CreateUserSchema, ResponseUserSchema


class UserRepository(BaseRepositoryImplementation):
    def __init__(self):
        super().__init__(
            model=UserModel,
            create_schema=CreateUserSchema,
            response_schema=ResponseUserSchema,
        )
