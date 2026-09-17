from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from domain.abstract_domain import AbstractDomain


@dataclass
class Product(AbstractDomain):

    bill_id: Optional[UUID] = None
    name: str = None
    quantity: int = 1
    unit_price: Decimal = Decimal("0")
    participant_ids: List[UUID] = field(default_factory=list)

    @property
    def total_price(self) -> Decimal:
        return self.unit_price * self.quantity
