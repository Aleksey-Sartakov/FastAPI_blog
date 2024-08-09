from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
	id: int
	first_name: str
	last_name: str
	email: str
	role_id: int


class UserCreate(schemas.BaseUserCreate):
	first_name: str
	last_name: str
	email: str
	password: str
	role_id: int


class UserUpdate(schemas.BaseUserUpdate):
	first_name: Optional[str] = None
	last_name: Optional[str] = None
	email: Optional[str] = None
	role_id: Optional[str] = None
