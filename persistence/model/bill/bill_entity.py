from sqlalchemy import Column, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship

from persistence.model.abstract_entity import AbstractEntity


class BillEntity(AbstractEntity):
    __tablename__ = "bills"

    owner_id = Column(ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False, default=0)

    products = relationship(
        "ProductEntity", back_populates="bill", cascade="all, delete-orphan"
    )
    participants = relationship(
        "ParticipantEntity", back_populates="bill", cascade="all, delete-orphan"
    )
