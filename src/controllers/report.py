from datetime import datetime
from io import BytesIO
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, Query
from starlette.responses import StreamingResponse

from src.models.user import UserRole
from src.services.report import ReportService
from src.utils.rbac import has_role


class ReportController:
    """Controlador para manejar las operaciones relacionadas con los reportes."""

    def __init__(self):
        self.service = ReportService()
        self.router = APIRouter(tags=["Reports"])

        @self.router.get("/top-products")
        async def get_top_products(
            start_date: datetime = Query(None),
            end_date: datetime = Query(None),
            limit: int = Query(10),
            _: dict = Depends(has_role([UserRole.administrador])),
        ) -> List[Dict[str, Any]]:
            """Obtiene los productos más vendidos en un período específico."""
            return self.service.get_top_products(start_date, end_date, limit)

        @self.router.get("/top-customers")
        async def get_top_customers(
            start_date: datetime = Query(None),
            end_date: datetime = Query(None),
            limit: int = Query(10),
            _: dict = Depends(has_role([UserRole.administrador])),
        ) -> List[Dict[str, Any]]:
            """Obtiene los clientes que más han gastado en un período específico."""
            return self.service.get_top_customers(start_date, end_date, limit)

        @self.router.get("/revenue")
        async def get_revenue_by_period(
            start_date: datetime = Query(None),
            end_date: datetime = Query(None),
            _: dict = Depends(has_role([UserRole.administrador])),
        ) -> Dict[str, Any]:
            """Obtiene los ingresos totales en un período específico."""
            return self.service.get_revenue_by_period(start_date, end_date)

        @self.router.get("/revenue/excel")
        async def get_excel_revenue_report(
            start_date: datetime = Query(...),
            end_date: datetime = Query(...),
            _: dict = Depends(has_role([UserRole.administrador])),
        ) -> StreamingResponse:
            """Genera un reporte de ingresos en formato Excel para un período específico."""
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
