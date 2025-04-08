import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.database import Database
from src.controllers.health_check import router as health_check_controller
from src.controllers.user import UserController


def create_fastapi_app():
    fastapi_app = FastAPI(
        title="FastAPI Application",
    )

    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    fastapi_app.include_router(health_check_controller, prefix="/health_check")
    fastapi_app.include_router(UserController().router, prefix="/user")

    return fastapi_app


def run_app(fastapi_app: FastAPI):
    uvicorn.run(fastapi_app, host="localhost", port=8000)


db = Database()
app = create_fastapi_app()
run_app(app)
