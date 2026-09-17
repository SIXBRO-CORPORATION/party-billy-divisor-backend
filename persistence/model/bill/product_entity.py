from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, Table
from sqlalchemy.orm import relationship

from persistence.model.abstract_entity import AbstractEntity, Base

product_participants = Table(
    "product_participants",
    Base.metadata,
    Column("product_id", ForeignKey("products.id"), primary_key=True),
    Column("participant_id", ForeignKey("participants.id"), primary_key=True),
)


class ProductEntity(AbstractEntity):
    __tablename__ = "products"

    bill_id = Column(ForeignKey("bills.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Numeric(10, 2), nullable=False, default=0)

    bill = relationship("BillEntity", back_populates="products")
    participants = relationship("ParticipantEntity", secondary=product_participants)
