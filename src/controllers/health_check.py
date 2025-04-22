from fastapi import APIRouter

from src.config.database import Database

router = APIRouter(tags=["Health Check"])
db = Database()


@router.get("/")
def health_check():
    if db.check_connection():
        return {"status": "OK"}

    return {"status": "ERROR"}
