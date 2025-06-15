from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from sqlalchemy.orm import Session

from src.models.base import BaseModel
from src.schemas.base import BaseSchema

T = TypeVar("T", bound=BaseModel)
S = TypeVar("S", bound=BaseSchema)


class BaseRepository(Generic[T, S], ABC):
    """Interfaz base para repositorios de datos."""

    @property
    @abstractmethod
    def session(self) -> Session:
        """Obtiene la sesión de la base de datos."""
        pass

    @property
    @abstractmethod
    def model(self) -> Type[T]:
        """Obtiene el modelo de la base de datos."""
        pass

    @property
    @abstractmethod
    def schema(self) -> Type[S]:
        """Obtiene el esquema de respuesta."""
        pass

    @abstractmethod
    def count_all(self) -> int:
        """Cuenta todos los registros en la base de datos."""
        pass

    @abstractmethod
    def count_all_by(self, field_name: str, field_value: Any) -> int:
        """Cuenta los registros por un campo específico."""
        pass

    @abstractmethod
    def find(self, id_key: int) -> S:
        """Encuentra un registro por su ID."""
        pass

    @abstractmethod
    def find_by(self, field_name: str, field_value: Any) -> Optional[S]:
        """Encuentra un registro por un campo específico."""
        pass

    @abstractmethod
    def find_all_by(
        self, field_name: str, field_value: Any, offset: int, limit: int
    ) -> List[S]:
        """Encuentra todos los registros por un campo específico y paginación."""
        pass

    @abstractmethod
    def find_all(self, offset: int = 0, limit: int = 10) -> List[S]:
        """Encuentra todos los registros con paginación."""
        pass

    @abstractmethod
    def save(self, model: T) -> S:
        """Guarda un nuevo registro en la base de datos."""
        pass

    @abstractmethod
    def update(self, id_key: int, changes: Dict[str, Any]) -> S:
        """Actualiza un registro existente en la base de datos."""
        pass

    @abstractmethod
    def remove(self, id_key: int) -> S:
        """Elimina un registro de la base de datos."""
        pass
