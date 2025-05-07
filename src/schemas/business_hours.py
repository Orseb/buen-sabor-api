from datetime import time

from src.models.business_hours import DayOfWeek
from src.schemas.base import BaseSchema


class BaseBusinessHoursSchema(BaseSchema):
    day: DayOfWeek
    opening_time: time
    closing_time: time
    is_active: bool = True


class CreateBusinessHoursSchema(BaseBusinessHoursSchema):
    pass


class ResponseBusinessHoursSchema(BaseBusinessHoursSchema):
    id_key: int
