from abc import ABC, abstractmethod
from typing import Generic, List, Type, TypeVar

from src.schemas.base import BaseSchema
from src.services.base import BaseService

S = TypeVar("S", bound=BaseSchema)


class BaseController(Generic[S], ABC):
    """Controlador base para manejar las operaciones CRUD de un recurso"""

    @property
    @abstractmethod
    def service(self) -> BaseService:
        """Devuelve el servicio asociado al controlador"""
        pass

    @property
    @abstractmethod
    def schema(self) -> Type[S]:
        """Devuelve el esquema asociado al controlador"""
        pass

    @abstractmethod
    def get_all(self, offset: int = 0, limit: int = 10) -> List[S]:
        """Obtiene una lista de todos los registros del recurso"""
        pass

    @abstractmethod
    def get_one(self, id_key: int) -> S:
        """Obtiene un registro específico del recurso por su ID"""
        pass

    @abstractmethod
    def save(self, schema: BaseSchema) -> S:
        """Guarda un nuevo registro del recurso"""
        pass

    @abstractmethod
    def update(self, id_key: int, schema: BaseSchema) -> S:
        """Actualiza un registro existente del recurso"""
        pass

    @abstractmethod
    def delete(self, id_key: int) -> S:
        """Elimina un registro del recurso por su ID"""
        pass

    def search_by_name(
        self, search_term: str, offset: int = 0, limit: int = 10
    ) -> List[S]:
        """Busca registros por nombre"""
        pass
