from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from domain.abstract_domain import AbstractDomain


@dataclass
class Participant(AbstractDomain):

    bill_id: Optional[UUID] = None
    name: str = None
