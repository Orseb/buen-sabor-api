from typing import Optional

from src.models.user import UserModel, UserRole
from src.repositories.user import UserRepository
from src.schemas.auth import GoogleUser
from src.schemas.user import CreateUserSchema, ResponseUserSchema
from src.services.base_implementation import BaseServiceImplementation


class UserService(BaseServiceImplementation[UserModel, ResponseUserSchema]):
    """Service for user operations."""

    def __init__(self):
        """Initialize the user service with repository and schemas."""
        super().__init__(
            repository=UserRepository(),
            model=UserModel,
            create_schema=CreateUserSchema,
            response_schema=ResponseUserSchema,
        )

    def create_or_update_user_from_google_info(
        self, google_user: GoogleUser
    ) -> ResponseUserSchema:
        """Create or update a user with information from Google OAuth."""
        user_email = google_user.email

        existing_user = self.get_one_by("email", user_email)
        if existing_user:
            return self.update(existing_user.id_key, {"google_sub": google_user.sub})

        new_user = CreateUserSchema(
            full_name=google_user.name,
            email=google_user.email,
            google_sub=google_user.sub,
            role=UserRole.cliente,
            active=True,
        )

        return self.save(new_user)

    def get_by_email(self, email: str) -> Optional[ResponseUserSchema]:
        """Get a user by email."""
        return self.get_one_by("email", email)

    def get_by_google_sub(self, google_sub: str) -> Optional[ResponseUserSchema]:
        """Get a user by Google sub."""
        return self.get_one_by("google_sub", google_sub)
