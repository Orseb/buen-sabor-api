from src.config.mercado_pago import sdk
from src.schemas.order import ResponseOrderSchema


def create_mp_preference(order: ResponseOrderSchema) -> str:
    preference_data = {
        "items": [
            {
                "title": "Producto de El Buen Sabor",
                "description": detail.manufactured_item.name,
                "quantity": detail.quantity,
                "unit_price": detail.unit_price,
            }
            for detail in order.details
        ]
    }

    preference_response = sdk.preference().create(preference_data)
    return preference_response["response"]["id"]
