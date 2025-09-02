from abc import ABC, abstractmethod
from typing import Optional
from domain.entities import User


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]: ...

    @abstractmethod
    async def create(self, email: str, hashed_password: str) -> User: ...

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]: ...