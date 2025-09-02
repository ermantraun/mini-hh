from abc import ABC, abstractmethod
from typing import Sequence
from domain.entities import ResumeImprovement


class IImprovementRepository(ABC):
    @abstractmethod
    async def create(self, resume_id: int, original: str, improved: str) -> ResumeImprovement: ...

    @abstractmethod
    async def list_for_resume(self, resume_id: int) -> Sequence[ResumeImprovement]: ...