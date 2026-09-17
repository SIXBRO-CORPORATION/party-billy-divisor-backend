from typing import Optional

from domain.user.user import User
from persistence.model.user.user_entity import UserEntity


class UserMapper:
    def to_domain(self, entity: Optional[UserEntity]) -> Optional[User]:
        if entity is None:
            return None

        return User(
            id=entity.id,
            name=entity.name,
            email=entity.email,
            password_hash=entity.password_hash,
            created_at=entity.created_at,
            modified_at=entity.modified_at,
            active=entity.active,
        )

    def to_entity(self, user: User) -> UserEntity:
        return UserEntity(
            id=user.id,
            name=user.name,
            email=user.email,
            password_hash=user.password_hash,
            created_at=user.created_at,
            modified_at=user.modified_at,
            active=user.active,
        )
