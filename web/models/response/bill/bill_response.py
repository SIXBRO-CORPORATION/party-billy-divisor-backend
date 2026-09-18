from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from web.models.response.bill.participant_response import ParticipantResponse
from web.models.response.bill.product_response import ProductResponse


class BillResponse(BaseModel):
    id: UUID
    title: str
    total_amount: Decimal
    created_at: Optional[datetime] = None
    products: List[ProductResponse]
    participants: List[ParticipantResponse]
