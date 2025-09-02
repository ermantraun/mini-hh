from .interfaces import IUserRepository
from .exceptions import RegistrationError, AuthenticationError
from application.security.password import hash_password, verify_password
from application.security.jwt import create_access_token


class AuthInteractor:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def register(self, email: str, password: str):
        existing = await self.repo.get_by_email(email)
        if existing:
            raise RegistrationError("Email already registered")
        return await self.repo.create(email, hash_password(password))

    async def login(self, email: str, password: str) -> str:
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise AuthenticationError("Invalid credentials")
        return create_access_token(str(user.id))