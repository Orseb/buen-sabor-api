from datetime import datetime
from io import BytesIO
from typing import Any, Dict, List

from src.repositories.inventory_purchase import InventoryPurchaseRepository
from src.repositories.invoice import InvoiceRepository
from src.repositories.order import OrderRepository
from src.repositories.order_detail import OrderDetailRepository
from src.repositories.order_inventory_detail import OrderInventoryDetailRepository
from src.utils.openpyxl import generate_excel_report


class ReportService:
    """Servicio para generar reportes de ventas, clientes y gastos."""

    def __init__(self):
        self.inventory_purchase_repository = InventoryPurchaseRepository()
        self.order_repository = OrderRepository()
        self.order_detail_repository = OrderDetailRepository()
        self.order_inventory_detail_repository = OrderInventoryDetailRepository()
        self.invoice_repository = InvoiceRepository()

    def get_top_products(
        self, start_date: datetime, end_date: datetime, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Obtiene los productos más vendidos en un rango de fechas."""
        manufactured_products = (
            self.order_detail_repository.get_top_manufactured_products(
                start_date, end_date, limit
            )
        )

        inventory_products = (
            self.order_inventory_detail_repository.get_top_inventory_products(
                start_date, end_date, limit
            )
        )

        all_products = manufactured_products + inventory_products
        all_products.sort(key=lambda x: x["quantity"], reverse=True)

        return all_products[:limit]

    def get_top_customers(
        self, start_date: datetime, end_date: datetime, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Obtiene los clientes con más compras en un rango de fechas."""
        return self.order_repository.get_top_customers(start_date, end_date, limit)

    def get_revenue_by_period(
        self, start_date: datetime, end_date: datetime
    ) -> Dict[str, Any]:
        """Obtiene los ingresos totales y gastos en un rango de fechas."""
        revenue_data = self.invoice_repository.get_revenue_by_period(
            start_date, end_date
        )

        purchases_data = self.inventory_purchase_repository.get_purchase_costs(
            start_date, end_date
        )

        total_revenue = revenue_data["total_revenue"]
        total_expenses = purchases_data["purchase_costs"]

        profit = total_revenue - total_expenses
        profit_margin = (profit / total_revenue * 100) if total_revenue > 0 else 0

        return {
            "revenue": total_revenue,
            "total_expenses": total_expenses,
            "profit": profit,
            "profit_margin_percentage": profit_margin,
            "total_invoices": revenue_data["invoice_count"],
            "total_inventory_purchases": purchases_data["purchase_count"],
            "start_date": start_date,
            "end_date": end_date,
        }

    def get_excel_revenue_report(
        self, start_date: datetime, end_date: datetime, buffer: BytesIO
    ) -> None:
        """Genera un reporte de ingresos en formato Excel."""
        purchases_data = self.inventory_purchase_repository.get_purchases_report_data(
            start_date, end_date
        )

        invoices_data = self.invoice_repository.get_invoices_report_data(
            start_date, end_date
        )

        generate_excel_report(buffer, purchases_data, invoices_data)
