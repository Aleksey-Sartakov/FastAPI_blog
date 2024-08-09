from datetime import datetime
from typing import Generator, AsyncGenerator, List, Annotated

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Session, mapped_column, sessionmaker
from sqlalchemy import TIMESTAMP, JSON, create_engine

from src.config import settings


intpk = Annotated[int, mapped_column(primary_key=True)]


class BaseDbModel(DeclarativeBase):
	type_annotation_map = {
		datetime: TIMESTAMP(),
		List[str]: JSON
	}

	def __repr__(self):
		columns = []
		for column in self.__table__.columns.keys():
			columns.append(f"{column} = {getattr(self, column)}")

		return f"{self.__class__.__name__} {{ {','.join(columns)} }}"


def get_session() -> Generator[Session, None, None]:
	engine = create_engine(settings.db_url_psycopg)
	session_maker = sessionmaker(engine, expire_on_commit=False)

	with session_maker() as session:
		yield session


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
	async_engine = create_async_engine(settings.db_url_asyncpg)
	async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)

	async with async_session_maker() as async_session:
		yield async_session
