from typing import Annotated

from fastapi import Depends

from business.auth.login_user_adapter import LoginUserAdapter
from business.auth.register_user_adapter import RegisterUserAdapter
from core.business.auth.login_user_port import LoginUserPort
from core.business.auth.register_user_port import RegisterUserPort
from core.persistence.user.user_repository_port import UserRepositoryPort
from core.security.jwt_provider_port import JWTProviderPort
from core.security.password_hasher_port import PasswordHasherPort
from web.dependencies.persistence_dependencies import get_user_repository
from web.dependencies.security_dependencies import get_jwt_provider, get_password_hasher


def get_register_user_port(
    user_repository: Annotated[UserRepositoryPort, Depends(get_user_repository)],
    password_hasher: Annotated[PasswordHasherPort, Depends(get_password_hasher)],
) -> RegisterUserPort:
    return RegisterUserAdapter(user_repository, password_hasher)


def get_login_user_port(
    user_repository: Annotated[UserRepositoryPort, Depends(get_user_repository)],
    password_hasher: Annotated[PasswordHasherPort, Depends(get_password_hasher)],
    jwt_provider: Annotated[JWTProviderPort, Depends(get_jwt_provider)],
) -> LoginUserPort:
    return LoginUserAdapter(user_repository, password_hasher, jwt_provider)
