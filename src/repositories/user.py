from typing import List

from src.models.user import UserModel, UserRole
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.user import CreateUserSchema, ResponseUserSchema


class UserRepository(BaseRepositoryImplementation):
    def __init__(self):
        super().__init__(
            model=UserModel,
            create_schema=CreateUserSchema,
            response_schema=ResponseUserSchema,
        )

    def count_all_employees(self) -> int:
        """Count all employees (users with non-client roles)."""
        with self.session_scope() as session:
            count = (
                session.query(self.model)
                .filter(self.model.role != UserRole.cliente)
                .filter(self.model.role != UserRole.administrador)
                .filter(self.model.active.is_(True))
                .count()
            )
            return count

    def count_all_clients(self) -> int:
        """Count all users with client roles."""
        with self.session_scope() as session:
            count = (
                session.query(self.model)
                .filter(self.model.role == UserRole.cliente)
                .filter(self.model.active.is_(True))
                .count()
            )
            return count

    def get_employees(
        self, offset: int = 0, limit: int = 10
    ) -> List[ResponseUserSchema]:
        """Get all employees (users with non-client roles)."""
        with self.session_scope() as session:
            employees = (
                session.query(self.model)
                .filter(self.model.role != UserRole.cliente)
                .filter(self.model.role != UserRole.administrador)
                .filter(self.model.active.is_(True))
                .offset(offset)
                .limit(limit)
                .all()
            )
            return [self.schema.model_validate(employee) for employee in employees]

    def get_clients(self, offset: int, limit: int) -> List[ResponseUserSchema]:
        """Get all users with client roles."""
        with self.session_scope() as session:
            clients = (
                session.query(self.model)
                .filter(self.model.role == UserRole.cliente)
                .filter(self.model.active.is_(True))
                .offset(offset)
                .limit(limit)
                .all()
            )
            return [self.schema.model_validate(client) for client in clients]

    def count_all_cookies(self) -> int:
        """Get all users with cook roles."""
        with self.session_scope() as session:
            count = (
                session.query(self.model)
                .filter(self.model.role == UserRole.cocinero)
                .filter(self.model.active.is_(True))
                .count()
            )
            return count
