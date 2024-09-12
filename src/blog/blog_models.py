from datetime import datetime
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from src.blog.schemas import ComplaintStatuses
from src.database_settings import BaseDbModel, intpk
from src.auth.auth_models import UserDbModel


class CategoryDbModel(BaseDbModel):
	__tablename__ = "category"

	id: Mapped[intpk]
	name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)

	articles: Mapped[List["ArticleDbModel"]] = relationship(back_populates="category", lazy="selectin")


class ArticleDbModel(BaseDbModel):
	__tablename__ = "article"

	id: Mapped[intpk]
	title: Mapped[str] = mapped_column(nullable=False)
	content: Mapped[str | None] = mapped_column(default=None)
	date_of_creation: Mapped[datetime] = mapped_column(default=datetime.utcnow)
	category_id: Mapped[int] = mapped_column(ForeignKey("category.id", ondelete="CASCADE"), nullable=False)
	user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

	creator: Mapped[UserDbModel] = relationship(back_populates="articles", lazy="joined")
	category: Mapped[CategoryDbModel] = relationship(back_populates="articles", lazy="joined")
	comments: Mapped[List["CommentDbModel"]] = relationship(back_populates="article", lazy="selectin")
	complaints: Mapped[List["ComplaintDbModel"]] = relationship(back_populates="article", lazy="selectin")


class CommentDbModel(BaseDbModel):
	__tablename__ = "comment"

	id: Mapped[intpk]
	content: Mapped[str] = mapped_column(nullable=False)
	date_of_creation: Mapped[datetime] = mapped_column(default=datetime.utcnow)
	user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
	article_id: Mapped[int] = mapped_column(ForeignKey("article.id", ondelete="CASCADE"), nullable=False)

	creator: Mapped[UserDbModel] = relationship(back_populates="comments", lazy="joined")
	article: Mapped[ArticleDbModel] = relationship(back_populates="comments", lazy="joined")


class ComplaintDbModel(BaseDbModel):
	__tablename__ = "complaint"

	id: Mapped[intpk]
	content: Mapped[str]
	status: Mapped[ComplaintStatuses] = mapped_column(nullable=False, default="in_processing")
	date_of_creation: Mapped[datetime] = mapped_column(default=datetime.utcnow)
	article_id: Mapped[int] = mapped_column(ForeignKey("article.id", ondelete="CASCADE"), nullable=False)
	user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

	article: Mapped[ArticleDbModel] = relationship(back_populates="complaints", lazy="joined")
	creator: Mapped[UserDbModel] = relationship(back_populates="articles", lazy="joined")
