from application.user.interfaces import IUserRepository
from application.resume.interfaces import IResumeRepository
from application.improvement.interfaces import IImprovementRepository
from domain.entities import User, Resume, ResumeImprovement
from datetime import datetime, timezone
from typing import Optional, Sequence, List

# Простые in-memory хранилища (только для тестов)
_users: dict[int, User] = {}
_resumes: dict[int, Resume] = {}
_improvements: dict[int, ResumeImprovement] = {}

_user_id = 1
_resume_id = 1
_improvement_id = 1

def _now():
    return datetime.now(timezone.utc)

class InMemoryUserRepository(IUserRepository):
    async def get_by_email(self, email: str) -> Optional[User]:
        return next((u for u in _users.values() if u.email == email), None)

    async def create(self, email: str, hashed_password: str) -> User:
        global _user_id
        u = User(id=_user_id, email=email, hashed_password=hashed_password, created_at=_now())
        _users[_user_id] = u
        _user_id += 1
        return u

    async def get_by_id(self, user_id: int) -> Optional[User]:
        return _users.get(user_id)

class InMemoryResumeRepository(IResumeRepository):
    async def create(self, user_id: int, title: str, content: str) -> Resume:
        global _resume_id
        r = Resume(id=_resume_id, user_id=user_id, title=title, content=content, created_at=_now(), updated_at=_now())
        _resumes[_resume_id] = r
        _resume_id += 1
        return r

    async def list_by_user(self, user_id: int) -> Sequence[Resume]:
        return sorted([r for r in _resumes.values() if r.user_id == user_id], key=lambda x: x.created_at, reverse=True)

    async def get(self, resume_id: int, user_id: int) -> Optional[Resume]:
        r = _resumes.get(resume_id)
        if r and r.user_id == user_id:
            return r
        return None

    async def update(self, resume_id: int, user_id: int, title: str, content: str) -> Optional[Resume]:
        r = await self.get(resume_id, user_id)
        if not r:
            return None
        nr = Resume(
            id=r.id,
            user_id=r.user_id,
            title=title,
            content=content,
            created_at=r.created_at,
            updated_at=_now(),
        )
        _resumes[r.id] = nr
        return nr

    async def delete(self, resume_id: int, user_id: int) -> bool:
        r = await self.get(resume_id, user_id)
        if not r:
            return False
        del _resumes[resume_id]
        # удаляем связанные улучшения
        to_del: List[int] = [iid for iid, imp in _improvements.items() if imp.resume_id == resume_id]
        for iid in to_del:
            del _improvements[iid]
        return True

class InMemoryImprovementRepository(IImprovementRepository):
    async def create(self, resume_id: int, original: str, improved: str) -> ResumeImprovement:
        global _improvement_id
        obj = ResumeImprovement(
            id=_improvement_id,
            resume_id=resume_id,
            original_content=original,
            improved_content=improved,
            created_at=_now(),
        )
        _improvements[_improvement_id] = obj
        _improvement_id += 1
        return obj

    async def list_for_resume(self, resume_id: int) -> Sequence[ResumeImprovement]:
        return sorted([i for i in _improvements.values() if i.resume_id == resume_id], key=lambda x: x.created_at, reverse=True)
