from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from domain.abstract_domain import AbstractDomain
from domain.bill.participant import Participant
from domain.bill.product import Product


@dataclass
class Bill(AbstractDomain):

    owner_id: Optional[UUID] = None
    title: str = None
    total_amount: Decimal = Decimal("0")
    products: List[Product] = field(default_factory=list)
    participants: List[Participant] = field(default_factory=list)
