from src.controllers.base_implementation import BaseControllerImplementation
from src.schemas.locality import (
    CreateLocalitySchema,
    ResponseLocalitySchema,
)
from src.services.locality import LocalityService


class LocalityController(BaseControllerImplementation):
    def __init__(self):
        super().__init__(
            create_schema=CreateLocalitySchema,
            response_schema=ResponseLocalitySchema,
            service=LocalityService(),
            tags=["Locality"],
        )
