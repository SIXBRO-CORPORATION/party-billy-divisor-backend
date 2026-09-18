from dataclasses import dataclass
from decimal import Decimal
from typing import List


@dataclass
class ProductSpec:

    name: str
    quantity: int
    unit_price: Decimal
    participant_names: List[str]
