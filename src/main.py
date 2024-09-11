from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth.auth_config import auth_backend
from src.auth.manager import fastapi_users
from src.auth.schemas import UserRead, UserCreate, UserUpdate
from src.blog.router import router_blog


tags_metadata = [
	{
		"name": "Auth",
		"description": """
			Basic authorization methods: registration, login, logout. The JWT key is used.
		""",
	},
	{
		"name": "Blog",
		"description": """
			Methods for working with all blog entities. Available only to authenticated users.
			For users who are not an admin (superuser), deleting other people's articles and comments is not available.
		""",
	},
	{
		"name": "Users",
		"description": """
			Methods for working with users. Available only to authenticated users.
			For users who are not an admin (superuser), only the "/users/me" methods are available.
		""",
	},
]


app = FastAPI(
	title="Technical Blog",
	openapi_tags=tags_metadata
)
app.include_router(
	fastapi_users.get_auth_router(auth_backend),
	prefix="/auth",
	tags=["Auth"],
)
app.include_router(
	fastapi_users.get_register_router(UserRead, UserCreate),
	prefix="/auth",
	tags=["Auth"],
)
app.include_router(
	fastapi_users.get_users_router(UserRead, UserUpdate),
	prefix="/users",
	tags=["Users"],
)
app.include_router(router_blog)

origins = [
	"http://localhost:8000",
]
app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
	allow_headers=[ "Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
				    "Authorization" ]
)
