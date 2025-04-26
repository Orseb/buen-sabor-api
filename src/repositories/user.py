from src.models.user import UserModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.user import UserSchema


class UserRepository(BaseRepositoryImplementation):
    def __init__(self):
        super().__init__(UserModel, UserSchema)

    def get_user_by_google_sub(self, google_sub: str) -> UserSchema | None:
        """
        Get a user by their google_sub.
        """
        with self.session_scope() as session:
            instance = (
                session.query(UserModel)
                .filter(UserModel.google_sub == str(google_sub))
                .first()
            )
            if instance is None:
                return None

            return self.schema.model_validate(instance)

    def get_user_by_email(self, email: str) -> UserSchema | None:
        """
        Get a user by their email.
        """
        with self.session_scope() as session:
            instance = session.query(UserModel).filter(UserModel.email == email).first()
            if instance is None:
                return None

            return self.schema.model_validate(instance)
