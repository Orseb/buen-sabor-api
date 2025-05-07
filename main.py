from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from src.config.database import Database
from src.config.settings import settings
from src.controllers.address import AddressController
from src.controllers.auth import router as auth_router
from src.controllers.business_hours import BusinessHoursController
from src.controllers.country import CountryController
from src.controllers.health_check import router as health_check_controller
from src.controllers.inventory_item import InventoryItemController
from src.controllers.inventory_item_category import InventoryItemCategoryController
from src.controllers.invoice import InvoiceController
from src.controllers.locality import LocalityController
from src.controllers.manufactured_item import ManufacturedItemController
from src.controllers.manufactured_item_category import (
    ManufacturedItemCategoryController,
)
from src.controllers.measurement_unit import MeasurementUnitController
from src.controllers.order import OrderController
from src.controllers.province import ProvinceController
from src.controllers.report import ReportController
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
app.include_router(auth_router, prefix="/auth")
app.include_router(CountryController().router, prefix="/country")
app.include_router(ProvinceController().router, prefix="/province")
app.include_router(LocalityController().router, prefix="/locality")
app.include_router(AddressController().router, prefix="/address")
app.include_router(MeasurementUnitController().router, prefix="/measurement_unit")
app.include_router(
    ManufacturedItemCategoryController().router, prefix="/manufactured_item_category"
)
app.include_router(
    InventoryItemCategoryController().router, prefix="/inventory_item_category"
)
app.include_router(InventoryItemController().router, prefix="/inventory_item")
app.include_router(UserController().router, prefix="/user")
app.include_router(ManufacturedItemController().router, prefix="/manufactured_item")
app.include_router(OrderController().router, prefix="/order")
app.include_router(InvoiceController().router, prefix="/invoice")
app.include_router(BusinessHoursController().router, prefix="/business_hours")
app.include_router(ReportController().router, prefix="/reports")
