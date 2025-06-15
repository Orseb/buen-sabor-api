from typing import Dict

from src.config.mercado_pago import sdk
from src.config.settings import settings
from src.schemas.order import ResponseOrderSchema


def create_mp_preference(order: ResponseOrderSchema) -> Dict[str, str]:
    """Creacion de la preferencia de pago de Mercado Pago."""
    items = []
    discount_factor = settings.pickup_discount if order.discount else 0

    def add_item(
        title: str, description: str, quantity: int, unit_price: float
    ) -> None:
        """Funcion helper para agregar un item a la preferencia."""
        items.append(
            {
                "title": title,
                "description": description,
                "quantity": quantity,
                "unit_price": unit_price - (unit_price * discount_factor),
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
