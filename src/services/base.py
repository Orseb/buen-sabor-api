from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union

from src.models.base import BaseModel
from src.repositories.base import BaseRepository
from src.schemas.base import BaseSchema
from src.schemas.pagination import PaginatedResponseSchema

T = TypeVar("T", bound=BaseModel)
S = TypeVar("S", bound=BaseSchema)


class BaseService(Generic[T, S], ABC):
    """Servicio base para manejar operaciones CRUD comunes"""

    @property
    @abstractmethod
    def repository(self) -> BaseRepository:
        """Repositorio asociado al servicio"""
        pass

    @property
    @abstractmethod
    def schema(self) -> Type[S]:
        """Esquema de validación asociado al servicio"""
        pass

    @property
    @abstractmethod
    def model(self) -> Type[T]:
        """Modelo asociado al servicio"""
        pass

    @abstractmethod
    def get_all(self, offset: int = 0, limit: int = 10) -> PaginatedResponseSchema:
        """Obtiene todos los registros con paginación"""
        pass

    @abstractmethod
    def get_one(self, id_key: int) -> S:
        """Obtiene un registro por su ID"""
        pass

    @abstractmethod
    def get_one_by(self, field_name: str, field_value: Any) -> Optional[S]:
        """Obtiene un registro por un campo específico"""
        pass

    @abstractmethod
    def get_all_by(
        self, field_name: str, field_value: Any, offset: int, limit: int
    ) -> PaginatedResponseSchema:
        """Obtiene todos los registros por un campo específico con paginación"""
        pass

    def search_by_name(
        self, search_term: str, offset: int = 0, limit: int = 10
    ) -> PaginatedResponseSchema:
        """Busca registros por nombre con paginación"""
        pass

    @abstractmethod
    def save(self, schema: Any) -> S:
        """Guarda un nuevo registro o actualiza uno existente"""
        pass

    @abstractmethod
    def update(self, id_key: int, schema_or_dict: Union[Any, Dict[str, Any]]) -> S:
        """Actualiza un registro existente"""
        pass

    @abstractmethod
    def delete(self, id_key: int) -> S:
        """Elimina un registro por su ID"""
        pass

    @abstractmethod
    def to_model(self, schema: Any) -> T:
        """Convierte un esquema a un modelo de base de datos"""
        pass
