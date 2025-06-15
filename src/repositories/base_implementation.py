from contextlib import contextmanager
from typing import Any, Dict, Generic, Iterator, List, Optional, Type, TypeVar

from sqlalchemy.orm import Session, scoped_session, sessionmaker

from src.config.database import Database
from src.models.base import BaseModel
from src.repositories.base import BaseRepository
from src.schemas.base import BaseSchema

T = TypeVar("T", bound=BaseModel)
S = TypeVar("S", bound=BaseSchema)


class RecordNotFoundError(Exception):
    """Excepción personalizada para indicar que no se encontró un registro."""

    pass


class BaseRepositoryImplementation(Generic[T, S], BaseRepository[T, S]):
    """Implementación base del repositorio genérico para manejar operaciones CRUD."""

    def __init__(
        self,
        model: Type[T],
        create_schema: Type[BaseSchema],
        response_schema: Type[S],
    ):
        self._model = model
        self._create_schema = create_schema
        self._response_schema = response_schema
        self._session_factory = scoped_session(sessionmaker(bind=Database().engine))

    @property
    def session(self):
        """Proporciona acceso a la sesión de la base de datos."""
        raise NotImplementedError(
            "Direct session access is not supported. Use session_scope()."
        )

    @property
    def model(self) -> Type[T]:
        """Devuelve el modelo asociado al repositorio."""
        return self._model

    @property
    def schema(self) -> Type[S]:
        """Devuelve el esquema de respuesta asociado al repositorio."""
        return self._response_schema

    @contextmanager
    def session_scope(self) -> Iterator[Session]:
        """Context manager para manejar la sesión de la base de datos."""
        session: Session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            print(f"Session rollback due to error: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def count_all(self) -> int:
        """Cuenta todos los registros activos en la tabla del modelo."""
        with self.session_scope() as session:
            return session.query(self.model).filter_by(active=True).count()

    def count_all_by(self, field_name: str, field_value: Any) -> int:
        """Cuenta los registros activos filtrados por un campo específico."""
        with self.session_scope() as session:
            return (
                session.query(self.model)
                .filter(getattr(self.model, field_name) == field_value)
                .filter_by(active=True)
                .count()
            )

    def find(self, id_key: int) -> S:
        """Busca un registro por su ID y devuelve el modelo validado por el esquema."""
        with self.session_scope() as session:
            model = session.get(self.model, id_key)
            if model is None or not getattr(model, "active", True):
                raise RecordNotFoundError(f"No record found with id {id_key}")
            return self.schema.model_validate(model)

    def find_by(self, field_name: str, field_value: Any) -> Optional[S]:
        """Busca un registro por un campo específico y devuelve modelo validado por el esquema."""
        with self.session_scope() as session:
            model = (
                session.query(self.model)
                .filter(getattr(self.model, field_name) == field_value)
                .filter_by(active=True)
                .first()
            )
            if model is None:
                return None
            return self.schema.model_validate(model)

    def find_all_by(
        self, field_name: str, field_value: Any, offset: int, limit: int
    ) -> List[S]:
        """Busca todos los registros activos filtrados por un campo específico."""
        with self.session_scope() as session:
            models = (
                session.query(self.model)
                .filter(getattr(self.model, field_name) == field_value)
                .filter_by(active=True)
                .offset(offset)
                .limit(limit)
                .all()
            )
            return [self.schema.model_validate(model) for model in models]

    def find_all(self, offset: int = 0, limit: int = 10) -> List[S]:
        """Busca todos los registros activos con paginación."""
        with self.session_scope() as session:
            models = (
                session.query(self.model)
                .filter_by(active=True)
                .offset(offset)
                .limit(limit)
                .all()
            )
            return [self.schema.model_validate(model) for model in models]

    def save(self, model: T) -> S:
        """Guarda un nuevo registro y devuelve el modelo validado por el esquema."""
        with self.session_scope() as session:
            session.add(model)
            session.flush()
            session.refresh(model)
            return self.schema.model_validate(model)

    def update(self, id_key: int, changes: Dict[str, Any]) -> S:
        """Actualiza un registro existente y devuelve el modelo validado por el esquema."""
        with self.session_scope() as session:
            model = session.get(self.model, id_key)
            if model is None:
                raise RecordNotFoundError(f"No record found with id {id_key}")

            for key, value in changes.items():
                if hasattr(model, key) and value is not None:
                    setattr(model, key, value)

            session.flush()
            session.refresh(model)
            return self.schema.model_validate(model)

    def remove(self, id_key: int) -> S:
        """Marca un registro como inactivo en lugar de eliminarlo físicamente."""
        with self.session_scope() as session:
            model = session.get(self.model, id_key)
            if model is None:
                raise RecordNotFoundError(f"No record found with id {id_key}")
            model.active = False
            session.add(model)
            session.flush()
            session.refresh(model)
            return self.schema.model_validate(model)
