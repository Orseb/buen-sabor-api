from datetime import datetime
from io import BytesIO

from fastapi import APIRouter, Depends, Query
from starlette.responses import StreamingResponse

from src.models.user import UserRole
from src.services.report import ReportService
from src.utils.rbac import has_role


class ReportController:
    def __init__(self):
        self.service = ReportService()
        self.router = APIRouter(tags=["Reports"])

        @self.router.get("/top-products")
        async def get_top_products(
            start_date: datetime = Query(...),
            end_date: datetime = Query(...),
            limit: int = Query(10),
            current_user: dict = Depends(has_role([UserRole.administrador])),
        ):
            return self.service.get_top_products(start_date, end_date, limit)

        @self.router.get("/top-customers")
        async def get_top_customers(
            start_date: datetime = Query(...),
            end_date: datetime = Query(...),
            limit: int = Query(10),
            current_user: dict = Depends(has_role([UserRole.administrador])),
        ):
            return self.service.get_top_customers(start_date, end_date, limit)

        @self.router.get("/revenue")
        async def get_revenue(
            start_date: datetime = Query(...),
            end_date: datetime = Query(...),
            current_user: dict = Depends(has_role([UserRole.administrador])),
        ):
            return self.service.get_revenue_by_period(start_date, end_date)

        @self.router.get("/revenue/excel")
        async def get_excel_revenue_report(
            start_date: datetime = Query(...),
            end_date: datetime = Query(...),
            current_user: dict = Depends(has_role([UserRole.administrador])),
        ):
            buffer = BytesIO()
            self.service.get_excel_revenue_report(start_date, end_date, buffer)
            buffer.seek(0)
            return StreamingResponse(
                buffer,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={
                    "Content-Disposition": f"attachment; filename=revenue_report_"
                    f"{start_date.strftime('%Y%m%d')}_to_{end_date.strftime('%Y%m%d')}"
                    f".xlsx"
                },
            )

        @self.router.get("/customer-orders/{user_id}")
        async def get_customer_orders(
            user_id: int,
            start_date: datetime = Query(...),
            end_date: datetime = Query(...),
            current_user: dict = Depends(has_role([UserRole.administrador])),
        ):
            return self.service.get_orders_by_customer(user_id, start_date, end_date)

        @self.router.get("/inventory-expenses")
        async def get_inventory_expenses(
            start_date: datetime = Query(...),
            end_date: datetime = Query(...),
            current_user: dict = Depends(has_role([UserRole.administrador])),
        ):
            return self.service.get_inventory_expenses(start_date, end_date)
