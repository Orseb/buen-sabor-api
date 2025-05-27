from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class MeasurementUnitModel(BaseModel):
    __tablename__ = "measurement_unit"

    name = Column(String, nullable=False)

    inventory_items = relationship(
        "InventoryItemModel", back_populates="measurement_unit"
    )
