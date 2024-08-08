from typing import AsyncGenerator
from config import settings

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from models import UserDbModel


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(settings.db_url_asyncpg)
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, UserDbModel)
