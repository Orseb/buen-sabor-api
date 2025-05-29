from typing import Any, Dict, List

from src.config.mercado_pago import sdk
from src.schemas.order import ResponseOrderSchema


def create_mp_preference(order: ResponseOrderSchema) -> dict:
    """Create a Mercado Pago preference for an order."""
    items: List[Dict[str, Any]] = []
    discount_factor = 0.9 if order.discount else 1.0

    def add_item(title, description, quantity, unit_price):
        items.append(
            {
                "title": title,
                "description": description,
                "quantity": quantity,
                "unit_price": unit_price * discount_factor,
                "currency_id": "ARS",
            }
        )

    for detail in order.details:
        add_item(
            f"El Buen Sabor - {detail.manufactured_item.name}",
            detail.manufactured_item.description or "Producto de El Buen Sabor",
            detail.quantity,
            detail.unit_price,
        )

    for detail in order.inventory_details:
        add_item(
            f"El Buen Sabor - {detail.inventory_item.name}",
            "Producto de El Buen Sabor",
            detail.quantity,
            detail.unit_price,
        )

    preference_response = sdk.preference().create({"items": items})

    return {
        "preference_id": preference_response["response"]["id"],
        "payment_url": preference_response["response"]["init_point"],
    }
