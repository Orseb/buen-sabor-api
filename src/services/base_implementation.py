from typing import Any, Generic, Optional, Type, TypeVar, cast

from src.models.base import BaseModel
from src.repositories.base import BaseRepository
from src.schemas.base import BaseSchema
from src.schemas.pagination import PaginatedResponseSchema
from src.services.base import BaseService

T = TypeVar("T", bound=BaseModel)
S = TypeVar("S", bound=BaseSchema)


class BaseServiceImplementation(Generic[T, S], BaseService[T, S]):
    """Implementación base del servicio para manejar operaciones CRUD comunes"""

    def __init__(
        self,
        repository: BaseRepository,
        model: Type[T],
        create_schema: Type[BaseSchema],
        response_schema: Type[S],
    ):

        self._repository = repository
        self._model = model
        self.create_schema = create_schema
        self.response_schema = response_schema

    @property
    def repository(self) -> BaseRepository:
        """Repositorio asociado al servicio"""
        return self._repository

    @property
    def schema(self) -> Type[S]:
        """Esquema de validación asociado al servicio"""
        return self.response_schema

    @property
    def model(self) -> Type[T]:
        """Modelo asociado al servicio"""
        return self._model

    def get_all(self, offset: int = 0, limit: int = 10) -> PaginatedResponseSchema:
        """Obtiene todos los registros con paginación"""
        total = self.repository.count_all()
        items = self.repository.find_all(offset, limit)
        return PaginatedResponseSchema(
            total=total, offset=offset, limit=limit, items=items
        )

    def get_one(self, id_key: int) -> S:
        """Obtiene un registro por su ID"""
        return self.repository.find(id_key)

    def get_one_by(self, field_name: str, field_value: Any) -> Optional[S]:
        """Obtiene un registro por un campo específico"""
        return self.repository.find_by(field_name, field_value)

    def get_all_by(
        self, field_name: str, field_value: Any, offset: int, limit: int
    ) -> PaginatedResponseSchema:
        """Obtiene todos los registros por un campo específico con paginación"""
        total = self.repository.count_all_by(field_name, field_value)
        items = self.repository.find_all_by(field_name, field_value, offset, limit)
        return PaginatedResponseSchema(
            total=total, offset=offset, limit=limit, items=items
        )

    def search_by_name(
        self, search_term: str, offset: int = 0, limit: int = 10
    ) -> PaginatedResponseSchema:
        """Busca registros por nombre con paginación"""
        total = self.repository.count_search_by_name(search_term)
        items = self.repository.search_by_name(search_term, offset, limit)
        return PaginatedResponseSchema(
            total=total, offset=offset, limit=limit, items=items
        )

    def save(self, schema: Any) -> S:
        """Guarda un nuevo registro o actualiza uno existente"""
        model_instance = self.to_model(schema)
        return self.repository.save(model_instance)

    def update(self, id_key: int, schema: Any) -> S:
        """Actualiza un registro existente"""
        changes = schema.model_dump(exclude_unset=True)
        return self.repository.update(id_key, changes)

    def delete(self, id_key: int) -> S:
        """Elimina un registro por su ID"""
        return self.repository.remove(id_key)

    def to_model(self, schema: Any) -> T:
        """Convierte un esquema a un modelo de base de datos"""
        model_class = self.model
        model_data = schema.model_dump(exclude_unset=True)
        model_instance = model_class(**model_data)
        return cast(T, model_instance)

    @repository.setter
    def repository(self, value: BaseRepository) -> None:
        """Establece el repositorio asociado al servicio"""
        self._repository = value

    @model.setter
    def model(self, value: Type[T]) -> None:
        """Establece el modelo asociado al servicio"""
        self._model = value

    @schema.setter
    def schema(self, value: Type[S]) -> None:
        """Establece el esquema de validación asociado al servicio"""
        self.response_schema = value
