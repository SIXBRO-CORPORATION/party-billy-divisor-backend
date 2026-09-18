from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class BillSummaryResponse(BaseModel):
    id: UUID
    title: str
    total_amount: Decimal
    created_at: Optional[datetime] = None
    participants_count: int
    paid_count: int
