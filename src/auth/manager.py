from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, FastAPIUsers

from src.auth.auth_config import auth_backend
from src.blog.blog_models import UserDbModel
from src.auth.utils import get_user_db

SECRET = "SECRET"


class UserManager(IntegerIDMixin, BaseUserManager[UserDbModel, int]):
	reset_password_token_secret = SECRET
	verification_token_secret = SECRET

	async def on_after_register(self, user: UserDbModel, request: Optional[Request] = None):
		print(f"User {user.id} has registered.")


async def get_user_manager(user_db=Depends(get_user_db)):
	yield UserManager(user_db)


fastapi_users = FastAPIUsers[UserDbModel, int](
	get_user_manager,
	[auth_backend],
)
