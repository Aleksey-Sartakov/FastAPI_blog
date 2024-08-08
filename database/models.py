from datetime import datetime
from typing import List, Annotated

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, TIMESTAMP, ForeignKey, JSON


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


class RoleDbModel(BaseDbModel):
	__tablename__ = "role"

	id: Mapped[intpk]
	name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
	permissions: Mapped[dict[str, List[str]]] = mapped_column(nullable=False)

	users: Mapped[List["UserDbModel"]] = relationship(back_populates="role")


class UserDbModel(SQLAlchemyBaseUserTable[int], BaseDbModel):
	id: Mapped[intpk]
	first_name: Mapped[str] = mapped_column(String(30), nullable=False)
	last_name: Mapped[str] = mapped_column(String(30), nullable=False)
	role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))

	role: Mapped[RoleDbModel] = relationship(back_populates="users", lazy="selectin")
	articles: Mapped[List["ArticleDbModel"]] = relationship(back_populates="creator")
	comments: Mapped[List["CommentDbModel"]] = relationship(back_populates="creator")


class CategoryDbModel(BaseDbModel):
	__tablename__ = "category"

	id: Mapped[intpk]
	name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)

	articles: Mapped[List["ArticleDbModel"]] = relationship(back_populates="category")


class ArticleDbModel(BaseDbModel):
	__tablename__ = "article"

	id: Mapped[intpk]
	title: Mapped[str] = mapped_column(nullable=False)
	content: Mapped[str | None]
	date_of_creation: Mapped[datetime] = mapped_column(default=datetime.utcnow)
	category_id: Mapped[int] = mapped_column(ForeignKey("category.id", ondelete="CASCADE"), nullable=False)
	user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

	creator: Mapped[UserDbModel] = relationship(back_populates="articles", lazy="selectin")
	category: Mapped[CategoryDbModel] = relationship(back_populates="articles", lazy="selectin")
	comments: Mapped[List["CommentDbModel"]] = relationship(back_populates="article")


class CommentDbModel(BaseDbModel):
	__tablename__ = "comment"

	id: Mapped[intpk]
	content: Mapped[str] = mapped_column(nullable=False)
	date_of_creation: Mapped[datetime] = mapped_column(default=datetime.utcnow)
	user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
	article_id: Mapped[int] = mapped_column(ForeignKey("article.id", ondelete="CASCADE"), nullable=False)

	creator: Mapped[UserDbModel] = relationship(back_populates="comments", lazy="selectin")
	article: Mapped[ArticleDbModel] = relationship(back_populates="comments", lazy="selectin")
