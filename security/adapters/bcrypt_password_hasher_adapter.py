import bcrypt

from core.security.password_hasher_port import PasswordHasherPort


class BcryptPasswordHasherAdapter(PasswordHasherPort):
    def hash(self, plain_password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(plain_password.encode("utf-8"), salt).decode("utf-8")

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        try:
            return bcrypt.checkpw(
                plain_password.encode("utf-8"), hashed_password.encode("utf-8")
            )
        except ValueError:
            # hash malformado/legado
            return False
