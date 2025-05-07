import enum

from sqlalchemy import Boolean, Column, Enum, Time

from src.models.base import BaseModel


class DayOfWeek(enum.Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"


class BusinessHoursModel(BaseModel):
    __tablename__ = "business_hours"

    day = Column(Enum(DayOfWeek), nullable=False)
    opening_time = Column(Time, nullable=False)
    closing_time = Column(Time, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
