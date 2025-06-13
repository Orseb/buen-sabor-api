from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class InventoryItemModel(BaseModel):
    __tablename__ = "inventory_item"

    name = Column(String, nullable=False, unique=True)
    current_stock = Column(Float, nullable=False)
    minimum_stock = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    purchase_cost = Column(Float, nullable=False)
    image_url = Column(String)
    is_ingredient = Column(Boolean, nullable=False)

    measurement_unit_id = Column(
        Integer, ForeignKey("measurement_unit.id_key", ondelete="CASCADE")
    )
    measurement_unit = relationship(
        "MeasurementUnitModel", back_populates="inventory_items"
    )

    category_id = Column(
        Integer,
        ForeignKey("inventory_item_category.id_key", ondelete="CASCADE"),
        nullable=False,
    )
    category = relationship(
        "InventoryItemCategoryModel", back_populates="inventory_items"
    )

    manufactured_item_details = relationship(
        "ManufacturedItemDetailModel", back_populates="inventory_item"
    )

    purchases = relationship("InventoryPurchaseModel", back_populates="inventory_item")

    order_inventory_details = relationship(
        "OrderInventoryDetailModel", back_populates="inventory_item"
    )
