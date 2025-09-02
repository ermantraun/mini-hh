from .interfaces import IResumeRepository
from .exceptions import ResumeNotFound
from domain.entities import Resume
from typing import Sequence


class ResumeInteractor:
    def __init__(self, repo: IResumeRepository):
        self.repo = repo

    async def create(self, user_id: int, title: str, content: str) -> Resume:
        return await self.repo.create(user_id, title, content)

    async def list_user(self, user_id: int) -> Sequence[Resume]:
        return await self.repo.list_by_user(user_id)

    async def get(self, user_id: int, resume_id: int) -> Resume:
        r = await self.repo.get(resume_id, user_id)
        if not r:
            raise ResumeNotFound()
        return r

    async def update(self, user_id: int, resume_id: int, title: str, content: str) -> Resume:
        r = await self.repo.update(resume_id, user_id, title, content)
        if not r:
            raise ResumeNotFound()
        return r

    async def delete(self, user_id: int, resume_id: int):
        ok = await self.repo.delete(resume_id, user_id)
        if not ok:
            raise ResumeNotFound()