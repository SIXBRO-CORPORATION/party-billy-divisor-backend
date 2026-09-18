from decimal import Decimal
from typing import List
from uuid import UUID

from pydantic import BaseModel


class ProductResponse(BaseModel):
    id: UUID
    name: str
    quantity: int
    unit_price: Decimal
    total_price: Decimal
    participant_ids: List[UUID]
