from typing import Dict

from fastapi import APIRouter

from src.config.database import Database


class HealthCheckController:
    """Controller para verificar la salud de la API y la conexión a la base de datos."""

    def __init__(self):
        self.router = APIRouter(tags=["Health Check"])
        self.db = Database()

        @self.router.get("/")
        def health_check() -> Dict[str, str]:
            """Endpoint para verificar la salud de la API y la conexión a la base de datos."""
            if self.db.check_connection():
                return {"status": "ok", "message": "Database connection is healthy"}

            return {"status": "error", "message": "Database connection failed"}
