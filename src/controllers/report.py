from datetime import datetime

from fastapi import APIRouter, Query

from src.services.report import ReportService


class ReportController:
    def __init__(self):
        self.service = ReportService()
        self.router = APIRouter(tags=["Reports"])

        @self.router.get("/top-products")
        async def get_top_products(
            start_date: datetime = Query(...),
            end_date: datetime = Query(...),
            limit: int = Query(10),
        ):
            return self.service.get_top_products(start_date, end_date, limit)

        @self.router.get("/top-customers")
        async def get_top_customers(
            start_date: datetime = Query(...),
            end_date: datetime = Query(...),
            limit: int = Query(10),
        ):
            return self.service.get_top_customers(start_date, end_date, limit)

        @self.router.get("/revenue")
        async def get_revenue(
            start_date: datetime = Query(...),
            end_date: datetime = Query(...),
        ):
            return self.service.get_revenue_by_period(start_date, end_date)

        @self.router.get("/customer-orders/{user_id}")
        async def get_customer_orders(
            user_id: int,
            start_date: datetime = Query(...),
            end_date: datetime = Query(...),
        ):
            return self.service.get_orders_by_customer(user_id, start_date, end_date)

        @self.router.get("/inventory-expenses")
        async def get_inventory_expenses(
            start_date: datetime = Query(...),
            end_date: datetime = Query(...),
        ):
            return self.service.get_inventory_expenses(start_date, end_date)
