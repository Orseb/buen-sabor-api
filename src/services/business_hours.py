from datetime import datetime
from typing import List, Optional

from src.models.business_hours import BusinessHoursModel, DayOfWeek
from src.repositories.business_hours import BusinessHoursRepository
from src.schemas.business_hours import (
    CreateBusinessHoursSchema,
    ResponseBusinessHoursSchema,
)
from src.services.base_implementation import BaseServiceImplementation


class BusinessHoursService(BaseServiceImplementation):
    def __init__(self):
        super().__init__(
            repository=BusinessHoursRepository(),
            model=BusinessHoursModel,
            create_schema=CreateBusinessHoursSchema,
            response_schema=ResponseBusinessHoursSchema,
        )

    def get_by_day(self, day: DayOfWeek) -> Optional[ResponseBusinessHoursSchema]:
        """Get business hours by day"""
        return self.repository.find_by_day(day)

    def get_all_active(self) -> List[ResponseBusinessHoursSchema]:
        """Get all active business hours"""
        return self.repository.find_all_active()

    def is_open_now(self) -> bool:
        """Check if the restaurant is open now"""
        now = datetime.now()
        day_of_week = now.strftime("%A").lower()
        current_time = now.time()

        # Get business hours for today
        business_hours = self.get_by_day(day_of_week)

        if not business_hours:
            return False

        # Check if current time is within business hours
        return (
            business_hours.opening_time <= current_time <= business_hours.closing_time
        )
