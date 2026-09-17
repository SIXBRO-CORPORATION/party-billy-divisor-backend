from core.business.auth.register_user_port import RegisterUserPort
from core.context import Context
from core.persistence.user.user_repository_port import UserRepositoryPort
from core.security.password_hasher_port import PasswordHasherPort
from domain.exceptions.business_exception import BusinessException
from domain.user.user import User


class RegisterUserAdapter(RegisterUserPort):
    def __init__(
        self,
        repository: UserRepositoryPort,
        password_hasher: PasswordHasherPort,
    ):
        self.repository = repository
        self.password_hasher = password_hasher

    async def execute(self, context: Context) -> User:
        data = context.get_data(User)

        if data is None or not data.email:
            raise BusinessException("Email é obrigatório")

        if not data.name:
            raise BusinessException("Nome é obrigatório")

        password = context.get_property("password", str)

        if not password:
            raise BusinessException("Senha é obrigatória")

        if len(password) < 8:
            raise BusinessException("A senha deve ter no mínimo 8 caracteres")

        email = data.email.strip().lower()

        if await self.repository.exists_by_email(email):
            raise BusinessException("Já existe uma conta cadastrada com esse email")

        new_user = User(
            name=data.name.strip(),
            email=email,
            password_hash=self.password_hasher.hash(password),
            active=True,
        )

        return await self.repository.save(new_user)
