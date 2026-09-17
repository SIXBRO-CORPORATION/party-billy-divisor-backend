from domain.user.user import User
from web.models.response.user.user_response import UserResponse


class UserModelMapper:
    def to_response(self, user: User) -> UserResponse:
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            created_at=user.created_at,
        )
