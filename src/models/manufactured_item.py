from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class ManufacturedItemModel(BaseModel):
    __tablename__ = "manufactured_item"

    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    preparation_time = Column(Integer, nullable=False)  # in minutes
    price = Column(Float, nullable=False)
    image_url = Column(String)
    recipe = Column(String)

    category_id = Column(
        Integer,
        ForeignKey("manufactured_item_category.id_key", ondelete="CASCADE"),
        nullable=False,
    )
    category = relationship(
        "ManufacturedItemCategoryModel", back_populates="manufactured_items"
    )

    details = relationship(
        "ManufacturedItemDetailModel", back_populates="manufactured_item"
    )
    order_details = relationship("OrderDetailModel", back_populates="manufactured_item")
