from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field


class CreateBillProductRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    quantity: int = Field(..., gt=0)
    unit_price: Decimal = Field(..., ge=0)
    participant_names: List[str] = Field(..., min_length=1)


class CreateBillRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    products: List[CreateBillProductRequest] = Field(..., min_length=1)
