from src.models.user import UserModel
from src.repositories.user import UserRepository
from src.schemas.user import UserSchema
from src.services.base_implementation import BaseServiceImplementation


class UserService(BaseServiceImplementation):

    def __init__(self):
        super().__init__(
            repository=UserRepository(), model=UserModel, schema=UserSchema
        )
        self.user_repository = UserRepository()

    async def get_user_by_google_sub(self, google_sub: str) -> UserSchema | None:
        """
        Get a user by their Google subscription ID.
        """
        return self.user_repository.get_user_by_google_sub(google_sub)
