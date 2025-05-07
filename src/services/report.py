from datetime import datetime
from typing import Dict, List

from sqlalchemy import desc, func

from src.models.inventory_item import InventoryItemModel
from src.models.invoice import InvoiceModel, InvoiceType
from src.models.manufactured_item import ManufacturedItemModel
from src.models.manufactured_item_detail import ManufacturedItemDetailModel
from src.models.order import OrderModel
from src.models.order_detail import OrderDetailModel
from src.models.user import UserModel
from src.repositories.invoice import InvoiceRepository
from src.repositories.order import OrderRepository
from src.repositories.order_detail import OrderDetailRepository


class ReportService:
    def __init__(self):
        self.order_repository = OrderRepository()
        self.order_detail_repository = OrderDetailRepository()
        self.invoice_repository = InvoiceRepository()

    def get_top_products(
        self, start_date: datetime, end_date: datetime, limit: int = 10
    ) -> List[Dict]:
        """Get top products by sales in a date range"""
        with self.order_detail_repository.session_scope() as session:
            results = (
                session.query(
                    OrderDetailModel.manufactured_item_id,
                    func.sum(OrderDetailModel.quantity).label("total_quantity"),
                )
                .join(OrderModel)
                .filter(
                    OrderModel.date >= start_date,
                    OrderModel.date <= end_date,
                    OrderModel.status == "facturado",
                )
                .group_by(OrderDetailModel.manufactured_item_id)
                .order_by(desc("total_quantity"))
                .limit(limit)
                .all()
            )

            top_products = []
            for result in results:
                manufactured_item = session.query(ManufacturedItemModel).get(result[0])
                top_products.append(
                    {
                        "id": manufactured_item.id_key,
                        "name": manufactured_item.name,
                        "quantity": result[1],
                        "category": manufactured_item.category.name,
                    }
                )

            return top_products

    def get_top_customers(
        self, start_date: datetime, end_date: datetime, limit: int = 10
    ) -> List[Dict]:
        """Get top customers by order count in a date range"""
        with self.order_repository.session_scope() as session:
            results = (
                session.query(
                    OrderModel.user_id,
                    func.count(OrderModel.id_key).label("order_count"),
                    func.sum(OrderModel.final_total).label("total_amount"),
                )
                .filter(
                    OrderModel.date >= start_date,
                    OrderModel.date <= end_date,
                    OrderModel.status == "facturado",
                )
                .group_by(OrderModel.user_id)
                .order_by(desc("order_count"))
                .limit(limit)
                .all()
            )

            top_customers = []
            for result in results:
                user = session.query(UserModel).get(result[0])
                top_customers.append(
                    {
                        "id": user.id_key,
                        "name": user.full_name,
                        "email": user.email,
                        "order_count": result[1],
                        "total_amount": result[2],
                    }
                )

            return top_customers

    def get_revenue_by_period(self, start_date: datetime, end_date: datetime) -> Dict:
        """Get revenue, costs and profit in a date range"""
        with self.invoice_repository.session_scope() as session:
            # Get total revenue (invoices minus credit notes)
            revenue_results = (
                session.query(func.sum(InvoiceModel.total).label("total_revenue"))
                .filter(
                    InvoiceModel.date >= start_date,
                    InvoiceModel.date <= end_date,
                    InvoiceModel.type == InvoiceType.factura,
                )
                .first()
            )

            credit_note_results = (
                session.query(func.sum(InvoiceModel.total).label("total_credit_notes"))
                .filter(
                    InvoiceModel.date >= start_date,
                    InvoiceModel.date <= end_date,
                    InvoiceModel.type == InvoiceType.nota_credito,
                )
                .first()
            )

            # Calculate costs (based on ingredients used in orders)
            costs_results = (
                session.query(
                    func.sum(
                        OrderDetailModel.quantity
                        * ManufacturedItemDetailModel.quantity
                        * InventoryItemModel.purchase_cost
                    ).label("total_costs")
                )
                .join(OrderModel)
                .join(ManufacturedItemModel)
                .join(ManufacturedItemDetailModel)
                .join(InventoryItemModel)
                .filter(
                    OrderModel.date >= start_date,
                    OrderModel.date <= end_date,
                    OrderModel.status == "facturado",
                )
                .first()
            )

            # Calculate totals
            total_revenue = revenue_results[0] or 0
            total_credit_notes = credit_note_results[0] or 0
            total_costs = costs_results[0] or 0

            net_revenue = total_revenue - total_credit_notes
            profit = net_revenue - total_costs

            return {
                "revenue": net_revenue,
                "costs": total_costs,
                "profit": profit,
                "start_date": start_date,
                "end_date": end_date,
            }

    def get_orders_by_customer(
        self, user_id: int, start_date: datetime, end_date: datetime
    ) -> List[Dict]:
        """Get all orders for a customer in a date range"""
        with self.order_repository.session_scope() as session:
            orders = (
                session.query(OrderModel)
                .filter(
                    OrderModel.user_id == user_id,
                    OrderModel.date >= start_date,
                    OrderModel.date <= end_date,
                )
                .order_by(desc(OrderModel.date))
                .all()
            )

            result = []
            for order in orders:
                invoice = (
                    session.query(InvoiceModel)
                    .filter(
                        InvoiceModel.order_id == order.id_key,
                        InvoiceModel.type == InvoiceType.factura,
                    )
                    .first()
                )

                result.append(
                    {
                        "id": order.id_key,
                        "date": order.date,
                        "total": order.final_total,
                        "status": order.status.value,
                        "invoice_number": invoice.number if invoice else None,
                        "invoice_id": invoice.id_key if invoice else None,
                    }
                )

            return result
