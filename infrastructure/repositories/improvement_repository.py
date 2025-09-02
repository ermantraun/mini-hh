from application.improvement.interfaces import IImprovementRepository
from domain.entities import ResumeImprovement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from infrastructure.db import models
from typing import Sequence


class ImprovementRepository(IImprovementRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, resume_id: int, original: str, improved: str) -> ResumeImprovement:
        obj = models.ResumeImprovementModel(
            resume_id=resume_id, original_content=original, improved_content=improved
        )
        self.session.add(obj)
        await self.session.flush()
        return ResumeImprovement(
            id=obj.id,
            resume_id=obj.resume_id,
            original_content=obj.original_content,
            improved_content=obj.improved_content,
            created_at=obj.created_at,
        )

    async def list_for_resume(self, resume_id: int) -> Sequence[ResumeImprovement]:
        res = await self.session.execute(
            select(models.ResumeImprovementModel)
            .where(models.ResumeImprovementModel.resume_id == resume_id)
            .order_by(models.ResumeImprovementModel.created_at.desc())
        )
        rows = res.scalars().all()
        return [
            ResumeImprovement(
                id=r.id,
                resume_id=r.resume_id,
                original_content=r.original_content,
                improved_content=r.improved_content,
                created_at=r.created_at,
            )
            for r in rows
        ]