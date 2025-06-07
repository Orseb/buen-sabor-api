from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class InvoiceDetailModel(BaseModel):
    __tablename__ = "invoice_detail"

    item_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    item_type = Column(String, nullable=False)

    invoice_id = Column(
        Integer,
        ForeignKey("invoice.id_key", ondelete="CASCADE"),
        nullable=False,
    )
    invoice = relationship("InvoiceModel", back_populates="details")

    manufactured_item_id = Column(
        Integer,
        ForeignKey("manufactured_item.id_key", ondelete="SET NULL"),
        nullable=True,
    )
    manufactured_item = relationship("ManufacturedItemModel")

    inventory_item_id = Column(
        Integer,
        ForeignKey("inventory_item.id_key", ondelete="SET NULL"),
        nullable=True,
    )
    inventory_item = relationship("InventoryItemModel")
