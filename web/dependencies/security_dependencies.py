from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.persistence.user.user_repository_port import UserRepositoryPort
from core.security.jwt_provider_port import JWTProviderPort
from core.security.password_hasher_port import PasswordHasherPort
from domain.exceptions.business_exception import BusinessException
from domain.user.user import User
from security.adapters.bcrypt_password_hasher_adapter import (
    BcryptPasswordHasherAdapter,
)
from security.adapters.jwt_provider_adapter import JWTProviderAdapter
from web.dependencies.persistence_dependencies import get_user_repository

security_scheme = HTTPBearer()


def get_jwt_provider() -> JWTProviderPort:
    return JWTProviderAdapter()


def get_password_hasher() -> PasswordHasherPort:
    return BcryptPasswordHasherAdapter()


async def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security_scheme)],
    jwt_provider: Annotated[JWTProviderPort, Depends(get_jwt_provider)],
) -> UUID:
    try:
        return jwt_provider.get_user_id_from_token(credentials.credentials)
    except BusinessException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    user_repository: Annotated[UserRepositoryPort, Depends(get_user_repository)],
) -> User:
    user = await user_repository.get(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado"
        )

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo. Entre em contato com o suporte.",
        )

    return user
