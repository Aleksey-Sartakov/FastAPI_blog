from datetime import datetime
from typing import AsyncGenerator, List, Annotated

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import TIMESTAMP, JSON

from src.config import settings


intpk = Annotated[int, mapped_column(primary_key=True)]


class BaseDbModel(DeclarativeBase):
	type_annotation_map = {
		datetime: TIMESTAMP(),
		dict[str, List[str]]: JSON
	}

	def __repr__(self):
		columns = []
		for column in self.__table__.columns.keys():
			columns.append(f"{column} = {getattr(self, column)}")

		return f"{self.__class__.__name__} {{ {','.join(columns)} }}"


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
	engine = create_async_engine(settings.db_url_asyncpg)
	async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

	async with async_session_maker() as session:
		yield session
