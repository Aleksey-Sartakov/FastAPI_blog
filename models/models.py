from datetime import datetime
from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON


metatdata = MetaData()


role = Table(
	"role",
	metatdata,
	Column("id", Integer, primary_key=True),
	Column("name", String, nullable=False),
	Column("permissions", JSON),
)

user = Table(
	"user",
	metatdata,
	Column("id", Integer, primary_key=True),
	Column("first_name", String, nullable=False),
	Column("last_name", String, nullable=False),
	Column("email", String, nullable=False),
	Column("password", String, nullable=False),
	Column("role_id", Integer, ForeignKey("role.id"), nullable=False),
)

category = Table(
	"category",
	metatdata,
	Column("id", Integer, primary_key=True),
	Column("name", String, nullable=False, unique=True),
)

article = Table(
	"article",
	metatdata,
	Column("id", Integer, primary_key=True),
	Column("title", String, nullable=False),
	Column("content", String),
	Column("user_id", Integer, ForeignKey("user.id"), nullable=False),
	Column("date_of_creation", TIMESTAMP, default=datetime.utcnow),
)

comment = Table(
	"comment",
	metatdata,
	Column("id", Integer, primary_key=True),
	Column("content", String, nullable=False),
	Column("article_id", Integer, ForeignKey("article.id"), nullable=False),
	Column("user_id", Integer, ForeignKey("user.id"), nullable=False),
	Column("date_of_creation", TIMESTAMP, default=datetime.utcnow),
)
