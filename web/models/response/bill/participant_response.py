from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class ParticipantResponse(BaseModel):
    id: UUID
    name: str
    amount_owed: Decimal
    paid: bool
