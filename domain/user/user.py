from dataclasses import dataclass
from typing import Optional

from domain.abstract_domain import AbstractDomain


@dataclass
class User(AbstractDomain):
    name: str = None
    email: str = None
    password_hash: Optional[str] = None
