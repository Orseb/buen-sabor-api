from typing import List

from sqlalchemy import func, select

from src.models.user import UserModel, UserRole
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.user import CreateUserSchema, ResponseUserSchema


class UserRepository(BaseRepositoryImplementation):
    """Repositorio para manejo de usuarios."""

    def __init__(self):
        super().__init__(
            model=UserModel,
            create_schema=CreateUserSchema,
            response_schema=ResponseUserSchema,
        )

    def count_all_employees(self) -> int:
        """Cuenta todos los empleados activos."""
        stmt = select(func.count()).where(
            self.model.active.is_(True),
            self.model.role != UserRole.cliente,
            self.model.role != UserRole.administrador,
        )
        with self.session_scope() as session:
            return session.scalar(stmt)

    def count_all_clients(self) -> int:
        """Cuenta todos los clientes activos."""
        stmt = select(func.count()).where(
            self.model.active.is_(True), self.model.role == UserRole.cliente
        )
        with self.session_scope() as session:
            return session.scalar(stmt)

    def get_employees(
        self, offset: int = 0, limit: int = 10
    ) -> List[ResponseUserSchema]:
        """Obtiene una lista de empleados activos."""
        stmt = (
            select(self.model)
            .where(
                self.model.active.is_(True),
                self.model.role != UserRole.cliente,
                self.model.role != UserRole.administrador,
            )
            .offset(offset)
            .limit(limit)
        )

        with self.session_scope() as session:
            result = session.execute(stmt)
            return [self.schema.model_validate(row) for row in result.scalars()]

    def get_clients(self, offset: int, limit: int) -> List[ResponseUserSchema]:
        """Obtiene una lista de clientes activos."""
        stmt = (
            select(self.model)
            .where(self.model.active.is_(True), self.model.role == UserRole.cliente)
            .offset(offset)
            .limit(limit)
        )

        with self.session_scope() as session:
            result = session.execute(stmt)
            return [self.schema.model_validate(row) for row in result.scalars()]

    def count_all_cookies(self) -> int:
        """Cuenta todos los cocineros activos."""
        stmt = select(func.count()).where(
            self.model.active.is_(True), self.model.role == UserRole.cocinero
        )
        with self.session_scope() as session:
            return session.scalar(stmt)

    def search_employees_by_name(
        self, search_term: str, offset: int, limit: int
    ) -> List[ResponseUserSchema]:
        """Busca empleados activos por nombre completo."""
        stmt = (
            select(self.model)
            .where(
                self.model.full_name.ilike(f"%{search_term}%"),
                self.model.active.is_(True),
                self.model.role != UserRole.cliente,
                self.model.role != UserRole.administrador,
            )
            .offset(offset)
            .limit(limit)
        )

        with self.session_scope() as session:
            result = session.execute(stmt)
            return [self.schema.model_validate(row) for row in result.scalars()]

    def count_search_employees_by_name(self, search_term: str) -> int:
        """Cuenta empleados activos que coinciden con el término de búsqueda."""
        stmt = select(func.count()).where(
            self.model.full_name.ilike(f"%{search_term}%"),
            self.model.active.is_(True),
            self.model.role != UserRole.cliente,
            self.model.role != UserRole.administrador,
        )
        with self.session_scope() as session:
            return session.scalar(stmt)

    def search_clients_by_name(
        self, search_term: str, offset: int, limit: int
    ) -> List[ResponseUserSchema]:
        """Busca clientes activos por nombre completo."""
        stmt = (
            select(self.model)
            .where(
                self.model.full_name.ilike(f"%{search_term}%"),
                self.model.active.is_(True),
                self.model.role == UserRole.cliente,
            )
            .offset(offset)
            .limit(limit)
        )

        with self.session_scope() as session:
            result = session.execute(stmt)
            return [self.schema.model_validate(row) for row in result.scalars()]

    def count_search_clients_by_name(self, search_term: str) -> int:
        """Cuenta clientes activos que coinciden con el término de búsqueda."""
        stmt = select(func.count()).where(
            self.model.full_name.ilike(f"%{search_term}%"),
            self.model.active.is_(True),
            self.model.role == UserRole.cliente,
        )
        with self.session_scope() as session:
            return session.scalar(stmt)
