from abc import ABC, abstractmethod
from uuid import UUID

from domain.auth.auth_token import AuthToken


class JWTProviderPort(ABC):
    @abstractmethod
    def create_access_token(self, user_id: UUID, email: str) -> AuthToken:
        pass

    @abstractmethod
    def get_user_id_from_token(self, token: str) -> UUID:
        pass
