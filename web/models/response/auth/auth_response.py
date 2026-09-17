from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from web.models.response.user.user_response import UserResponse


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: Optional[datetime] = None
    user: UserResponse
