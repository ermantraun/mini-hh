from application.resume.interfaces import IResumeRepository
from domain.entities import Resume
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from infrastructure.db import models
from typing import Optional, Sequence


class ResumeRepository(IResumeRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: int, title: str, content: str) -> Resume:
        obj = models.ResumeModel(user_id=user_id, title=title, content=content)
        self.session.add(obj)
        await self.session.flush()
        return Resume(
            id=obj.id,
            user_id=obj.user_id,
            title=obj.title,
            content=obj.content,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
        )

    async def list_by_user(self, user_id: int) -> Sequence[Resume]:
        res = await self.session.execute(
            select(models.ResumeModel).where(models.ResumeModel.user_id == user_id).order_by(models.ResumeModel.created_at.desc())
        )
        items = res.scalars().all()
        return [
            Resume(
                id=r.id,
                user_id=r.user_id,
                title=r.title,
                content=r.content,
                created_at=r.created_at,
                updated_at=r.updated_at,
            )
            for r in items
        ]

    async def get(self, resume_id: int, user_id: int) -> Optional[Resume]:
        res = await self.session.execute(
            select(models.ResumeModel).where(
                models.ResumeModel.id == resume_id, models.ResumeModel.user_id == user_id
            )
        )
        r = res.scalar_one_or_none()
        if not r:
            return None
        return Resume(
            id=r.id,
            user_id=r.user_id,
            title=r.title,
            content=r.content,
            created_at=r.created_at,
            updated_at=r.updated_at,
        )

    async def update(self, resume_id: int, user_id: int, title: str, content: str) -> Optional[Resume]:
        await self.session.execute(
            update(models.ResumeModel)
            .where(models.ResumeModel.id == resume_id, models.ResumeModel.user_id == user_id)
            .values(title=title, content=content)
        )
        await self.session.flush()
        return await self.get(resume_id, user_id)

    async def delete(self, resume_id: int, user_id: int) -> bool:
        res = await self.session.execute(
            delete(models.ResumeModel).where(models.ResumeModel.id == resume_id, models.ResumeModel.user_id == user_id)
        )
        return res.rowcount > 0