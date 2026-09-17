from datetime import datetime, timedelta
from uuid import UUID

from jose import JWTError, jwt

from core.security.jwt_provider_port import JWTProviderPort
from domain.auth.auth_token import AuthToken
from domain.exceptions.business_exception import BusinessException
from security.config import settings


class JWTProviderAdapter(JWTProviderPort):
    def __init__(self):
        self.secret_key = settings.jwt_secret_key
        self.algorithm = settings.jwt_algorithm
        self.expire_minutes = settings.jwt_access_token_expire_minutes

    def create_access_token(self, user_id: UUID, email: str) -> AuthToken:
        expire = datetime.utcnow() + timedelta(minutes=self.expire_minutes)

        payload = {
            "sub": str(user_id),
            "email": email,
            "exp": expire,
            "iat": datetime.utcnow(),
        }

        encoded_jwt = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

        return AuthToken(
            access_token=encoded_jwt,
            token_type="bearer",
            expires_at=expire,
            user_id=user_id,
        )

    def get_user_id_from_token(self, token: str) -> UUID:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except JWTError as e:
            raise BusinessException(f"Token inválido ou expirado: {str(e)}")

        subject = payload.get("sub")

        if subject is None:
            raise BusinessException("Token inválido")

        return UUID(subject)
