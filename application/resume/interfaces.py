from abc import ABC, abstractmethod
from typing import Optional, Sequence
from domain.entities import Resume


class IResumeRepository(ABC):
    @abstractmethod
    async def create(self, user_id: int, title: str, content: str) -> Resume: ...

    @abstractmethod
    async def list_by_user(self, user_id: int) -> Sequence[Resume]: ...

    @abstractmethod
    async def get(self, resume_id: int, user_id: int) -> Optional[Resume]: ...

    @abstractmethod
    async def update(self, resume_id: int, user_id: int, title: str, content: str) -> Optional[Resume]: ...

    @abstractmethod
    async def delete(self, resume_id: int, user_id: int) -> bool: ...