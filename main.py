from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.database import Database
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

app.include_router(health_check_controller, prefix="/health_check")
app.include_router(UserController().router, prefix="/user")
