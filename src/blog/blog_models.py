from datetime import datetime
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from src.database_settings import BaseDbModel, intpk
from src.auth.auth_models import UserDbModel


class CategoryDbModel(BaseDbModel):
	__tablename__ = "category"

	id: Mapped[intpk]
	name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)

	articles: Mapped[List["ArticleDbModel"]] = relationship(back_populates="category", cascade="all, delete")


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
	comments: Mapped[List["CommentDbModel"]] = relationship(back_populates="article", cascade="all, delete")


class CommentDbModel(BaseDbModel):
	__tablename__ = "comment"

	id: Mapped[intpk]
	content: Mapped[str] = mapped_column(nullable=False)
	date_of_creation: Mapped[datetime] = mapped_column(default=datetime.utcnow)
	user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
	article_id: Mapped[int] = mapped_column(ForeignKey("article.id", ondelete="CASCADE"), nullable=False)

	creator: Mapped[UserDbModel] = relationship(back_populates="comments", lazy="selectin")
	article: Mapped[ArticleDbModel] = relationship(back_populates="comments", lazy="selectin")
