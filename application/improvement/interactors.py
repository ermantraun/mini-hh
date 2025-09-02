from application.improvement.interfaces import IImprovementRepository
from application.resume.interfaces import IResumeRepository
from application.resume.exceptions import ResumeNotFound
from domain.entities import ResumeImprovement
from typing import Sequence


class ImprovementInteractor:
    def __init__(self, imp_repo: IImprovementRepository, resume_repo: IResumeRepository):
        self.imp_repo = imp_repo
        self.resume_repo = resume_repo

    async def improve(self, user_id: int, resume_id: int) -> ResumeImprovement:
        resume = await self.resume_repo.get(resume_id, user_id)
        if not resume:
            raise ResumeNotFound()
        improved = resume.content + " [Improved]"
        return await self.imp_repo.create(resume.id, resume.content, improved)

    async def list_improvements(self, user_id: int, resume_id: int) -> Sequence[ResumeImprovement]:
        resume = await self.resume_repo.get(resume_id, user_id)
        if not resume:
            raise ResumeNotFound()
        return await self.imp_repo.list_for_resume(resume_id)