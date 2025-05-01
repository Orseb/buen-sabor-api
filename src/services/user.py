from src.models.user import UserModel
from src.repositories.user import UserRepository
from src.schemas.auth import GoogleUser
from src.schemas.user import CreateUserSchema, ResponseUserSchema
from src.services.base_implementation import BaseServiceImplementation


class UserService(BaseServiceImplementation):

    def __init__(self):
        super().__init__(
            repository=UserRepository(),
            model=UserModel,
            create_schema=CreateUserSchema,
            response_schema=ResponseUserSchema,
        )

    def create_or_update_user_from_google_info(
        self, google_user: GoogleUser
    ) -> ResponseUserSchema:
        """
        Creates user with obtained info from google login
        """
        user_email = google_user.email

        existing_user = self.repository.find_by("email", user_email)
        if existing_user:
            return self.repository.update(
                existing_user.id_key, {"google_sub": google_user.sub}
            )

        return self.save(
            CreateUserSchema(
                full_name=google_user.name,
                email=google_user.email,
                google_sub=google_user.sub,
            )
        )
