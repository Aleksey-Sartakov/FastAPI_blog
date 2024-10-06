from datetime import datetime
from typing import Optional, Annotated, Literal

from fastapi import Depends
from pydantic import BaseModel, field_validator, PositiveInt, NonNegativeInt


ComplaintStatuses = Literal["in_processing", "rejected", "confirmed"]
OrderingMethods = Literal["asc", "desc"]


class ArticleCreate(BaseModel):
	title: str
	category_id: int
	content: Optional[str] = None


class ArticleRead(BaseModel):
	id: int
	title: str
	content: str
	date_of_creation: datetime
	category_id: int
	user_id: int

	@field_validator("date_of_creation")
	@classmethod
	def date_to_string(cls, date_instance: datetime) -> str:
		return date_instance.strftime("%Y-%m-%d %H:%M")


class CommentCreate(BaseModel):
	content: str
	article_id: int


class CommentRead(BaseModel):
	id: int
	content: str
	date_of_creation: datetime
	article_id: int
	user_id: int

	@field_validator("date_of_creation")
	@classmethod
	def date_to_string(cls, date_instance: datetime) -> str:
		return date_instance.strftime("%Y-%m-%d %H:%M")


class CategoryRead(BaseModel):
	id: int
	name: str


class ComplaintCreateModel(BaseModel):
	content: str
	article_id: int


class ComplaintReadModel(BaseModel):
	id: int
	content: str
	status: ComplaintStatuses
	date_of_creation: datetime
	article_id: int
	user_id: int

	@field_validator("date_of_creation")
	@classmethod
	def date_to_string(cls, date_instance: datetime) -> str:
		return date_instance.strftime("%Y-%m-%d %H:%M")


class Pagination(BaseModel):
	limit: PositiveInt = 100
	offset: NonNegativeInt = 0


PaginationDependency = Annotated[Pagination, Depends()]
