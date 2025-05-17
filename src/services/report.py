from datetime import datetime
from typing import Any, Dict, List

from sqlalchemy import desc, func

from src.models.inventory_item import InventoryItemModel
from src.models.inventory_purchase import InventoryPurchaseModel
from src.models.invoice import InvoiceModel, InvoiceType
from src.models.manufactured_item import ManufacturedItemModel
from src.models.order import OrderModel
from src.models.order_detail import OrderDetailModel
from src.models.user import UserModel
from src.repositories.invoice import InvoiceRepository
from src.repositories.order import OrderRepository
from src.repositories.order_detail import OrderDetailRepository


class ReportService:
    """Service for generating business reports."""

    def __init__(self):
        """Initialize the report service with repositories."""
        self.order_repository = OrderRepository()
        self.order_detail_repository = OrderDetailRepository()
        self.invoice_repository = InvoiceRepository()

    def get_top_products(
        self, start_date: datetime, end_date: datetime, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get top products by sales in a date range."""
        with self.order_detail_repository.session_scope() as session:
            results = (
                session.query(
                    OrderDetailModel.manufactured_item_id,
                    func.sum(OrderDetailModel.quantity).label("total_quantity"),
                    func.sum(OrderDetailModel.subtotal).label("total_revenue"),
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
                if manufactured_item:
                    top_products.append(
                        {
                            "id": manufactured_item.id_key,
                            "name": manufactured_item.name,
                            "quantity": result[1],
                            "revenue": result[2],
                            "category": (
                                manufactured_item.category.name
                                if manufactured_item.category
                                else "Unknown"
                            ),
                        }
                    )

            return top_products

    def get_top_customers(
        self, start_date: datetime, end_date: datetime, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get top customers by order count in a date range."""
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
                if user:
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

    def get_revenue_by_period(
        self, start_date: datetime, end_date: datetime
    ) -> Dict[str, Any]:
        """Get revenue, costs and profit in a date range."""
        with self.invoice_repository.session_scope() as session:
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

            purchase_costs_results = (
                session.query(
                    func.sum(InventoryPurchaseModel.total_cost).label("purchase_costs")
                )
                .filter(
                    InventoryPurchaseModel.purchase_date >= start_date,
                    InventoryPurchaseModel.purchase_date <= end_date,
                )
                .first()
            )

            total_revenue = revenue_results[0] or 0
            total_credit_notes = credit_note_results[0] or 0
            total_expenses = purchase_costs_results[0] or 0

            net_revenue = total_revenue - total_credit_notes
            profit = net_revenue - total_expenses
            profit_margin = (profit / net_revenue * 100) if net_revenue > 0 else 0

            return {
                "revenue": net_revenue,
                "total_expenses": total_expenses,
                "profit": profit,
                "profit_margin_percentage": profit_margin,
                "start_date": start_date,
                "end_date": end_date,
            }

    def get_orders_by_customer(
        self, user_id: int, start_date: datetime, end_date: datetime
    ) -> List[Dict[str, Any]]:
        """Get all orders for a customer in a date range."""
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
                        "status": order.status.value if order.status else None,
                        "invoice_number": invoice.number if invoice else None,
                        "invoice_id": invoice.id_key if invoice else None,
                        "payment_method": (
                            order.payment_method.value if order.payment_method else None
                        ),
                        "is_paid": order.is_paid,
                    }
                )

            return result

    def get_inventory_expenses(
        self, start_date: datetime, end_date: datetime
    ) -> Dict[str, Any]:
        """Get inventory purchase expenses in a date range."""
        with self.invoice_repository.session_scope() as session:
            purchase_results = (
                session.query(
                    func.sum(InventoryPurchaseModel.total_cost).label("total_cost"),
                    func.count(InventoryPurchaseModel.id_key).label("purchase_count"),
                )
                .filter(
                    InventoryPurchaseModel.purchase_date >= start_date,
                    InventoryPurchaseModel.purchase_date <= end_date,
                )
                .first()
            )

            # Get top purchased items
            top_items_results = (
                session.query(
                    InventoryPurchaseModel.inventory_item_id,
                    func.sum(InventoryPurchaseModel.quantity).label("total_quantity"),
                    func.sum(InventoryPurchaseModel.total_cost).label("total_cost"),
                )
                .filter(
                    InventoryPurchaseModel.purchase_date >= start_date,
                    InventoryPurchaseModel.purchase_date <= end_date,
                )
                .group_by(InventoryPurchaseModel.inventory_item_id)
                .order_by(desc("total_cost"))
                .limit(5)
                .all()
            )

            top_items = []
            for result in top_items_results:
                inventory_item = session.query(InventoryItemModel).get(result[0])
                if inventory_item:
                    top_items.append(
                        {
                            "id": inventory_item.id_key,
                            "name": inventory_item.name,
                            "quantity": result[1],
                            "total_cost": result[2],
                        }
                    )

            total_cost = purchase_results[0] or 0
            purchase_count = purchase_results[1] or 0

            return {
                "total_expenses": total_cost,
                "purchase_count": purchase_count,
                "top_purchased_items": top_items,
                "start_date": start_date,
                "end_date": end_date,
            }
