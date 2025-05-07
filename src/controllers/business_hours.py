from typing import List

from src.controllers.base_implementation import BaseControllerImplementation
from src.models.business_hours import DayOfWeek
from src.schemas.business_hours import (
    CreateBusinessHoursSchema,
    ResponseBusinessHoursSchema,
)
from src.services.business_hours import BusinessHoursService


class BusinessHoursController(BaseControllerImplementation):
    def __init__(self):
        super().__init__(
            create_schema=CreateBusinessHoursSchema,
            response_schema=ResponseBusinessHoursSchema,
            service=BusinessHoursService(),
            tags=["Business Hours"],
        )

        @self.router.get("/active", response_model=List[ResponseBusinessHoursSchema])
        async def get_active_hours():
            return self.service.get_all_active()

        @self.router.get("/day/{day}", response_model=ResponseBusinessHoursSchema)
        async def get_by_day(day: DayOfWeek):
            return self.service.get_by_day(day)

        @self.router.get("/is-open")
        async def is_open_now():
            return {"is_open": self.service.is_open_now()}
