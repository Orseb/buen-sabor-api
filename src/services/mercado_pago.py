from typing import Any, Dict, List

from src.config.mercado_pago import sdk
from src.schemas.order import ResponseOrderSchema


def create_mp_preference(order: ResponseOrderSchema) -> str:
    """Create a Mercado Pago preference for an order."""
    items: List[Dict[str, Any]] = []
    for detail in order.details:
        items.append(
            {
                "title": f"El Buen Sabor - {detail.manufactured_item.name}",
                "description": detail.manufactured_item.description
                or "Producto de El Buen Sabor",
                "quantity": detail.quantity,
                "unit_price": detail.unit_price,
                "currency_id": "ARS",
            }
        )

    preference_response = sdk.preference().create({"items": items})

    return preference_response["response"]["id"]
