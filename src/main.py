from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers
from fastapi.middleware.cors import CORSMiddleware

from src.auth.auth_config import auth_backend
from src.auth.manager import get_user_manager
from src.auth.schemas import UserRead, UserCreate, UserUpdate
from src.blog.blog_models import UserDbModel

fastapi_users = FastAPIUsers[UserDbModel, int](
	get_user_manager,
	[auth_backend],
)

app = FastAPI(
	title="Technical Blog"
)
app.include_router(
	fastapi_users.get_auth_router(auth_backend),
	prefix="/auth",
	tags=["auth"],
)
app.include_router(
	fastapi_users.get_register_router(UserRead, UserCreate),
	prefix="/auth",
	tags=["auth"],
)
app.include_router(
	fastapi_users.get_users_router(UserRead, UserUpdate),
	prefix="/users",
	tags=["users"],
)

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

current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: UserDbModel = Depends(current_user)):
	return f"Hello, {user.email}"


@app.get("/get_categories")
def get_categories():
	return


@app.get("/get_articles_by_category_id")
def get_articles_by_category_id(category_id: int):
	return


@app.get("/get_articles_by_user_id")
def get_articles_by_user_id(user_id: int):
	return


@app.get("/get_comments_by_article_id")
def get_comments_by_article_id(article_id: int):
	return


@app.post("/create_article")
def create_article():
	return


@app.post("/create_comment")
def create_comment():
	return


@app.post("/create_user")
def create_user():
	return


@app.delete("/delete_user/{user_id}")
def delete_user(user_id: int):
	return


@app.delete("/delete_article/{article_id}")
def delete_article(article_id: int):
	return


@app.delete("/delete_comment/{comment_id}")
def delete_comment(comment_id: int):
	return
