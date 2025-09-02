from dishka import Provider, Scope, provide, make_async_container
from api.config import get_config, Config
from infrastructure.db.database import get_engine, get_session_factory
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, async_sessionmaker
from application.user.interfaces import IUserRepository
from application.resume.interfaces import IResumeRepository
from application.improvement.interfaces import IImprovementRepository
from infrastructure.repositories.user_repository import UserRepository
from infrastructure.repositories.resume_repository import ResumeRepository
from infrastructure.repositories.improvement_repository import ImprovementRepository
from application.user.interactors import AuthInteractor
from application.resume.interactors import ResumeInteractor
from application.improvement.interactors import ImprovementInteractor
from typing import AsyncIterator
import sys

IS_PYTEST = "pytest" in sys.modules

class CoreProvider(Provider):
    scope = Scope.APP

    @provide
    def config(self) -> Config:
        return get_config()

    @provide
    def engine(self) -> AsyncEngine:
        return get_engine()

    @provide
    def session_factory(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return get_session_factory(engine)

class SessionProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def session(self, session_factory: async_sessionmaker[AsyncSession]) -> AsyncIterator[AsyncSession]:
        async with session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

class RepoProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def user_repo(self, session: AsyncSession) -> IUserRepository:
        return UserRepository(session)

    @provide
    def resume_repo(self, session: AsyncSession) -> IResumeRepository:
        return ResumeRepository(session)

    @provide
    def improvement_repo(self, session: AsyncSession) -> IImprovementRepository:
        return ImprovementRepository(session)

class ConfigOnlyProvider(Provider):
    scope = Scope.APP

    @provide
    def config(self) -> Config:
        return get_config()

class InMemoryRepoProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def user_repo(self) -> IUserRepository:
        from infrastructure.repositories.inmemory import InMemoryUserRepository
        return InMemoryUserRepository()

    @provide
    def resume_repo(self) -> IResumeRepository:
        from infrastructure.repositories.inmemory import InMemoryResumeRepository
        return InMemoryResumeRepository()

    @provide
    def improvement_repo(self) -> IImprovementRepository:
        from infrastructure.repositories.inmemory import InMemoryImprovementRepository
        return InMemoryImprovementRepository()

class InteractorsProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def auth_interactor(self, user_repo: IUserRepository) -> AuthInteractor:
        return AuthInteractor(user_repo)

    @provide
    def resume_interactor(self, resume_repo: IResumeRepository) -> ResumeInteractor:
        return ResumeInteractor(resume_repo)

    @provide
    def improvement_interactor(
        self,
        improvement_repo: IImprovementRepository,
        resume_repo: IResumeRepository,
    ) -> ImprovementInteractor:
        return ImprovementInteractor(improvement_repo, resume_repo)

def build_container():
    if IS_PYTEST:
        return make_async_container(ConfigOnlyProvider(), InMemoryRepoProvider(), InteractorsProvider())
    return make_async_container(CoreProvider(), SessionProvider(), RepoProvider(), InteractorsProvider())