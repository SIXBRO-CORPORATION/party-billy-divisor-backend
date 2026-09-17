from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from persistence.model.abstract_entity import AbstractEntity


class ParticipantEntity(AbstractEntity):
    __tablename__ = "participants"

    bill_id = Column(ForeignKey("bills.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)

    bill = relationship("BillEntity", back_populates="participants")
