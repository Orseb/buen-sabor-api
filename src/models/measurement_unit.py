from sqlalchemy import Boolean, Column, String

from src.models.base import BaseModel


class MeasurementUnitModel(BaseModel):
    __tablename__ = "measurement_unit"

    name = Column(String, nullable=False)
    active = Column(Boolean, nullable=False)
