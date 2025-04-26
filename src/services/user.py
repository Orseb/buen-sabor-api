from src.models.user import UserModel
from src.repositories.user import UserRepository
from src.schemas.auth import GoogleUser
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

    async def create_or_update_user_from_google_info(
        self, google_user: GoogleUser
    ) -> UserSchema:
        """
        Creates user with obtained info from google login
        """
        user_email = google_user.email

        existing_user = self.user_repository.get_user_by_email(user_email)
        if existing_user:
            return self.user_repository.update(
                existing_user.id_key, {"google_sub": google_user.sub}
            )

        new_user = UserModel(
            full_name=google_user.name,
            email=google_user.email,
            google_sub=google_user.sub,
            role="cliente",
            active=True,
        )

        return self.user_repository.save(new_user)
