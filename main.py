from fastapi import FastAPI


app = FastAPI(
	title="Technical Blog"
)


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