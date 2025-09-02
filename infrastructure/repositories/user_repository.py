from application.user.interfaces import IUserRepository
from domain.entities import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from infrastructure.db import models
from typing import Optional


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> Optional[User]:
        res = await self.session.execute(select(models.UserModel).where(models.UserModel.email == email))
        obj = res.scalar_one_or_none()
        if obj:
            return User(id=obj.id, email=obj.email, hashed_password=obj.hashed_password, created_at=obj.created_at)
        return None

    async def create(self, email: str, hashed_password: str) -> User:
        u = models.UserModel(email=email, hashed_password=hashed_password)
        self.session.add(u)
        await self.session.flush()
        return User(id=u.id, email=u.email, hashed_password=u.hashed_password, created_at=u.created_at)

    async def get_by_id(self, user_id: int) -> Optional[User]:
        res = await self.session.execute(select(models.UserModel).where(models.UserModel.id == user_id))
        obj = res.scalar_one_or_none()
        if obj:
            return User(id=obj.id, email=obj.email, hashed_password=obj.hashed_password, created_at=obj.created_at)
        return None