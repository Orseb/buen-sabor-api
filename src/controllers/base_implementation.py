from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from fastapi import APIRouter, Depends

from src.controllers.base import BaseController
from src.models.user import UserRole
from src.schemas.base import BaseSchema
from src.schemas.pagination import PaginatedResponseSchema
from src.services.base import BaseService
from src.utils.rbac import get_current_user, has_role

S = TypeVar("S", bound=BaseSchema)
C = TypeVar("C", bound=BaseSchema)


class BaseControllerImplementation(Generic[S, C], BaseController[S]):
    """Controlador base para implementar operaciones CRUD estándar"""

    def __init__(
        self,
        create_schema: Type[C],
        response_schema: Type[S],
        service: BaseService,
        tags: Optional[List[str]] = None,
        required_roles: Optional[List[UserRole]] = None,
    ):
        self._service = service
        self.create_schema = create_schema
        self.response_schema = response_schema
        self.router = APIRouter(tags=tags or [])

        if required_roles is None:
            required_roles = [UserRole.administrador, UserRole.cocinero]

        role_dependency = has_role(required_roles)

        @self.router.get("/", response_model=PaginatedResponseSchema)
        async def get_all(
            offset: int = 0,
            limit: int = 10,
            _: Dict[str, Any] = Depends(get_current_user),
        ) -> PaginatedResponseSchema:
            """Obtiene todos los registros paginados"""
            return self.get_all(offset, limit)

        @self.router.get("/{id_key}", response_model=self.response_schema)
        async def get_one(
            id_key: int, _: Dict[str, Any] = Depends(get_current_user)
        ) -> S:
            """Obtiene un registro por su ID"""
            return self.get_one(id_key)

        @self.router.post("/", response_model=self.response_schema)
        async def save(
            schema_in: self.create_schema,
            _: Dict[str, Any] = Depends(role_dependency),
        ) -> S:
            """Guarda un nuevo registro"""
            return self.save(schema_in)

        @self.router.put("/{id_key}", response_model=self.response_schema)
        async def update(
            id_key: int,
            schema_in: self.create_schema,
            _: Dict[str, Any] = Depends(role_dependency),
        ) -> S:
            """Actualiza un registro existente por su ID"""
            return self.update(id_key, schema_in)

        @self.router.delete("/{id_key}")
        async def delete(
            id_key: int, _: Dict[str, Any] = Depends(role_dependency)
        ) -> S:
            """Elimina un registro por su ID"""
            return self.delete(id_key)

    @property
    def service(self) -> BaseService:
        """Devuelve el servicio asociado al controlador"""
        return self._service

    @property
    def schema(self) -> Type[S]:
        """Devuelve el esquema de respuesta asociado al controlador"""
        return self.response_schema

    def get_all(self, offset: int = 0, limit: int = 10) -> PaginatedResponseSchema:
        """Obtiene todos los registros paginados"""
        return self.service.get_all(offset, limit)

    def get_one(self, id_key: int) -> S:
        """Obtiene un registro por su ID"""
        return self.service.get_one(id_key)

    def save(self, schema: C) -> S:
        """Guarda un nuevo registro"""
        return self.service.save(schema)

    def update(self, id_key: int, schema: C) -> S:
        """Actualiza un registro existente por su ID"""
        return self.service.update(id_key, schema)

    def delete(self, id_key: int) -> S:
        """Elimina un registro por su ID"""
        return self.service.delete(id_key)

    @schema.setter
    def schema(self, value: Type[S]) -> None:
        """Establece el esquema de respuesta del controlador"""
        self.response_schema = value

    @service.setter
    def service(self, value: BaseService) -> None:
        """Establece el servicio asociado al controlador"""
        self._service = value
