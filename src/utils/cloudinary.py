import base64

import cloudinary.uploader

from src.config.settings import settings

cloudinary.config(
    cloud_name="dwemmfiw3",
    api_key="789196988949882",
    api_secret=settings.cloudinary_api_key,
    secure=True,
)


def upload_base64_image_to_cloudinary(base64_str, folder):
    if "," in base64_str:
        base64_str = base64_str.split(",")[1]
    image_data = base64.b64decode(base64_str)
    result = cloudinary.uploader.upload(image_data, folder=folder)
    return result["secure_url"]
