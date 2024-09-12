from typing import List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from src.database_settings import BaseDbModel, intpk


class RoleDbModel(BaseDbModel):
	__tablename__ = "role"

	id: Mapped[intpk]
	name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
	permissions: Mapped[List[str]] = mapped_column(nullable=False)

	users: Mapped[List["UserDbModel"]] = relationship(back_populates="role", lazy="selectin")


class UserDbModel(SQLAlchemyBaseUserTable[int], BaseDbModel):
	id: Mapped[intpk]
	first_name: Mapped[str] = mapped_column(String(30), nullable=False)
	last_name: Mapped[str] = mapped_column(String(30), nullable=False)
	role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))

	role: Mapped[RoleDbModel] = relationship(back_populates="users", lazy="joined")
	articles: Mapped[List["ArticleDbModel"]] = relationship(back_populates="creator", lazy="selectin")
	comments: Mapped[List["CommentDbModel"]] = relationship(back_populates="creator", lazy="selectin")
	complaints: Mapped[List["ComplaintDbModel"]] = relationship(back_populates="creator", lazy="selectin")
