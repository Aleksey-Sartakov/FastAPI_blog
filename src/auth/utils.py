from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from src.database_settings import get_async_session
from src.blog.blog_models import UserDbModel


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
	yield SQLAlchemyUserDatabase(session, UserDbModel)
