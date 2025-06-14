import base64

import cloudinary.uploader

from src.config.settings import settings

cloudinary.config(
    cloud_name="dwemmfiw3",
    api_key="789196988949882",
    api_secret=settings.cloudinary_api_key,
    secure=True,
)


def upload_base64_image_to_cloudinary(base64_str: str, folder: str) -> str:
    """Sube una imagen en formato base64 a Cloudinary y devuelve la URL de la misma."""
    if "," in base64_str:
        base64_str = base64_str.split(",")[1]

    image_data = base64.b64decode(base64_str)
    result = cloudinary.uploader.upload(image_data, folder=folder)
    return result["secure_url"]


def delete_image_from_cloudinary(image_url: str) -> None:
    """Elimina una imagen de Cloudinary usando su URL."""
    public_id = image_url.split("/")[-1].split(".")[0]
    cloudinary.uploader.destroy(f"manufactured_items/{public_id}")
