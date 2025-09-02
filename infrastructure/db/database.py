from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from api.config import get_config


def get_engine():
    return create_async_engine(get_config().postgres.async_url, echo=False, future=True)


def get_session_factory(engine):
    return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)