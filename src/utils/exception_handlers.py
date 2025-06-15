from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from psycopg2.errors import ForeignKeyViolation, UniqueViolation
from sqlalchemy.exc import IntegrityError

from src.repositories.base_implementation import RecordNotFoundError


async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    """Manejador de excepciones HTTP personalizado."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def not_found_error_handler(_: Request, exc: RecordNotFoundError) -> JSONResponse:
    """Manejador de excepciones para registros no encontrados."""
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


async def value_error_handler(_: Request, exc: ValueError) -> JSONResponse:
    """Manejador de excepciones para errores de valor."""
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


async def integrity_error_handler(_: Request, exc: IntegrityError) -> JSONResponse:
    """Manejador de excepciones para errores de integridad en la base de datos."""
    if isinstance(exc.orig, ForeignKeyViolation):
        return JSONResponse(
            status_code=400,
            content={"detail": "Llave foranea no válida."},
        )
    if isinstance(exc.orig, UniqueViolation):
        return JSONResponse(
            status_code=400,
            content={"detail": "El registro ya existe."},
        )
    return JSONResponse(
        status_code=500,
        content={"detail": "Error de integridad en la base de datos."},
    )


async def global_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    """Manejador de excepciones global para errores no controlados."""
    return JSONResponse(
        status_code=500,
        content={"detail": f"Error interno del servidor: {str(exc)}"},
    )
