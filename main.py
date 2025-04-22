from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from src.config.database import Database
from src.config.settings import settings
from src.controllers.auth import router as auth_router
from src.controllers.health_check import router as health_check_controller
from src.controllers.user import UserController

db = Database()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

app.include_router(health_check_controller, prefix="/health_check")
app.include_router(UserController().router, prefix="/user")
app.include_router(auth_router, prefix="/auth")
