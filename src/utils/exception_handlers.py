from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from psycopg2.errors import ForeignKeyViolation, UniqueViolation
from sqlalchemy.exc import IntegrityError

from src.repositories.base_implementation import RecordNotFoundError


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def not_found_error_handler(
    request: Request, exc: RecordNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


async def integrity_error_handler(
    request: Request, exc: IntegrityError
) -> JSONResponse:
    if isinstance(exc.orig, ForeignKeyViolation):
        return JSONResponse(
            status_code=400,
            content={"detail": "Foreign key constraint violated."},
        )
    if isinstance(exc.orig, UniqueViolation):
        return JSONResponse(
            status_code=400,
            content={"detail": "Unique constraint violated."},
        )
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected database error occurred."},
    )


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."},
    )
