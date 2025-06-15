from src.models.user import UserModel, UserRole
from src.repositories.user import UserRepository
from src.schemas.auth import GoogleUser
from src.schemas.pagination import PaginatedResponseSchema
from src.schemas.user import CreateUserSchema, ResponseUserSchema
from src.services.base_implementation import BaseServiceImplementation
from src.utils.cloudinary import upload_base64_image_to_cloudinary


class UserService(BaseServiceImplementation[UserModel, ResponseUserSchema]):
    """Servicio para manejar la lógica de negocio relacionada con los usuarios."""

    def __init__(self):

        super().__init__(
            repository=UserRepository(),
            model=UserModel,
            create_schema=CreateUserSchema,
            response_schema=ResponseUserSchema,
        )

    def update(self, id_key: int, schema: CreateUserSchema) -> ResponseUserSchema:
        """Actualiza un usuario existente y maneja la imagen si es necesario."""
        user = self.repository.find(id_key)
        if schema.image_url and schema.image_url != user.image_url:
            schema.image_url = upload_base64_image_to_cloudinary(
                schema.image_url, "users"
            )
        return super().update(id_key, schema)

    def create_or_update_user_from_google_info(
        self, google_user: GoogleUser
    ) -> ResponseUserSchema:
        """Crea o actualiza un usuario basado en la información de Google."""
        existing_user = self.repository.find_by("email", google_user.email)
        if existing_user:
            return self.repository.update(
                existing_user.id_key, {"google_sub": google_user.sub}
            )

        new_user = CreateUserSchema(
            full_name=google_user.name,
            email=google_user.email,
            google_sub=google_user.sub,
            role=UserRole.cliente,
            active=True,
        )

        return self.save(new_user)

    def get_employees(self, offset: int, limit: int) -> PaginatedResponseSchema:
        """Obtiene una lista paginada de empleados."""
        total = self.repository.count_all_employees()
        items = self.repository.get_employees(offset, limit)
        return PaginatedResponseSchema(
            total=total, offset=offset, limit=limit, items=items
        )

    def get_clients(self, offset: int, limit: int) -> PaginatedResponseSchema:
        """Obtiene una lista paginada de clientes."""
        total = self.repository.count_all_clients()
        items = self.repository.get_clients(offset, limit)
        return PaginatedResponseSchema(
            total=total, offset=offset, limit=limit, items=items
        )

    def update_employee_password(
        self, id_key: int, new_password: str
    ) -> ResponseUserSchema:
        """Actualiza la contraseña de un empleado."""
        return self.repository.update(
            id_key, {"password": new_password, "first_login": False}
        )
