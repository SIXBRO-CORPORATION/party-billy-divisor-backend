from core.business.auth.login_user_port import LoginUserPort
from core.context import Context
from core.persistence.user.user_repository_port import UserRepositoryPort
from core.security.jwt_provider_port import JWTProviderPort
from core.security.password_hasher_port import PasswordHasherPort
from domain.auth.auth_token import AuthToken
from domain.exceptions.business_exception import BusinessException


class LoginUserAdapter(LoginUserPort):
    def __init__(
        self,
        repository: UserRepositoryPort,
        password_hasher: PasswordHasherPort,
        jwt_provider: JWTProviderPort,
    ):
        self.repository = repository
        self.password_hasher = password_hasher
        self.jwt_provider = jwt_provider

    async def execute(self, context: Context) -> AuthToken:
        email = context.get_property("email", str)
        password = context.get_property("password", str)

        if not email or not password:
            raise BusinessException("Email e senha são obrigatórios")

        user = await self.repository.find_by_email(email.strip().lower())

        invalid_credentials = BusinessException("Email ou senha inválidos")

        if user is None or not user.password_hash:
            raise invalid_credentials

        if not self.password_hasher.verify(password, user.password_hash):
            raise invalid_credentials

        if not user.active:
            raise BusinessException("Usuário inativo. Entre em contato com o suporte.")

        context.put_property("user", user)

        return self.jwt_provider.create_access_token(user_id=user.id, email=user.email)
