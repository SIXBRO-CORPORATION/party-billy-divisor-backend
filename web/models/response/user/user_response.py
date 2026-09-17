from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: UUID
    name: Optional[str] = None
    email: Optional[str] = None
    created_at: Optional[datetime] = None
