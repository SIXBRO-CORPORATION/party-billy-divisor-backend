from core.command import Command
from domain.auth.auth_token import AuthToken


class LoginUserPort(Command[AuthToken]):
    pass
