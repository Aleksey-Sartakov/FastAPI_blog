import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager, lazyload

from src.blog.custom_exceptions import AccessForbiddenException
from src.blog.blog_models import CategoryDbModel, ArticleDbModel, CommentDbModel, ComplaintDbModel
from src.blog.schemas import (
	CategoryRead, ArticleCreate, ArticleRead, CommentCreate, CommentRead, PaginationDependency, OrderingMethods,
	ComplaintCreateModel, ComplaintReadModel
)

from src.database_settings import get_async_session

from src.auth.manager import fastapi_users
from src.auth.auth_models import UserDbModel


current_user = fastapi_users.current_user()
current_active_user = fastapi_users.current_user(active=True)
current_superuser_user = fastapi_users.current_user(active=True, superuser=True)
router_blog = APIRouter(prefix="/blog", tags=["Blog"])


@router_blog.get("/categories")
async def get_all_categories(session: AsyncSession = Depends(get_async_session)):
	try:
		query = select(CategoryDbModel)
		result = await session.execute(query)
		result_orm = result.scalars().all()

		json_results = json.dumps([CategoryRead.model_validate(row, from_attributes=True).model_dump() for row in result_orm])

		return {
			"status": "success",
			"data": json_results,
			"details": None
		}

	except Exception as e:
		raise HTTPException(status_code=500, detail={
			"status": "error",
			"data": None,
			"details": str(e)
		})


@router_blog.get("/articles_by_category")
async def get_articles_by_category(
		category_id: int,
		pagination: PaginationDependency,
		order: OrderingMethods = "asc",
		session: AsyncSession = Depends(get_async_session)
):
	try:
		if order == "asc":
			order_rule = ArticleDbModel.date_of_creation.asc
		else:
			order_rule = ArticleDbModel.date_of_creation.desc

		query = (
			select(ArticleDbModel)
			.filter_by(category_id=category_id)
			.limit(pagination.limit)
			.offset(pagination.offset)
			.order_by(order_rule())
		)

		result = await session.execute(query)
		result_orm = result.scalars().all()
		json_results = json.dumps([ArticleRead.model_validate(row, from_attributes=True).model_dump() for row in result_orm])

		return {
			"status": "success",
			"data": json_results,
			"details": None
		}

	except Exception as e:
		raise HTTPException(status_code=500, detail={
			"status": "error",
			"data": None,
			"details": str(e)
		})


@router_blog.get("/articles_of_current_user", dependencies=[Depends(current_active_user)])
async def get_articles_of_current_user(
		pagination: PaginationDependency,
		order: OrderingMethods = "asc",
		session: AsyncSession = Depends(get_async_session),
		user: UserDbModel = Depends(current_user)
):
	try:
		if order == "asc":
			order_rule = ArticleDbModel.date_of_creation.asc
		else:
			order_rule = ArticleDbModel.date_of_creation.desc

		query = (
			select(ArticleDbModel)
			.filter_by(user_id=user.id)
			.limit(pagination.limit)
			.offset(pagination.offset)
			.order_by(order_rule())
		)

		result = await session.execute(query)
		result_orm = result.scalars().all()
		json_results = json.dumps([ArticleRead.model_validate(row, from_attributes=True).model_dump() for row in result_orm])

		return {
			"status": "success",
			"data": json_results,
			"details": None
		}

	except Exception as e:
		raise HTTPException(status_code=500, detail={
			"status": "error",
			"data": None,
			"details": str(e)
		})


@router_blog.get("/article_content")
async def get_article_content(
		article_id: int,
		session: AsyncSession = Depends(get_async_session)
):
	try:
		query = (
			select(ArticleDbModel.content)
			.filter_by(id=article_id)
		)
		query = query
		result = await session.execute(query)
		result_orm = result.scalars().all()

		return {
			"status": "success",
			"data": result_orm[0],
			"details": None
		}

	except IndexError as e:
		raise HTTPException(status_code=400, detail={
			"status": "error",
			"data": None,
			"details": "There are no articles with this id."
		})

	except Exception as e:
		raise HTTPException(status_code=500, detail={
			"status": "error",
			"data": None,
			"details": str(e)
		})


@router_blog.get("/comments")
async def get_comments_by_article(
		article_id: int,
		pagination: PaginationDependency,
		order: OrderingMethods = "asc",
		session: AsyncSession = Depends(get_async_session)):
	try:
		if order == "asc":
			order_rule = CommentDbModel.date_of_creation.asc
		else:
			order_rule = CommentDbModel.date_of_creation.desc

		query = (
			select(CommentDbModel)
			.filter_by(article_id=article_id)
			.limit(pagination.limit)
			.offset(pagination.offset)
			.order_by(order_rule())
		)

		result = await session.execute(query)
		result_orm = result.scalars().all()
		json_results = json.dumps([CommentRead.model_validate(row, from_attributes=True).model_dump() for row in result_orm])

		return {
			"status": "success",
			"data": json_results,
			"details": None
		}

	except Exception as e:
		raise HTTPException(status_code=500, detail={
			"status": "error",
			"data": None,
			"details": str(e)
		})


@router_blog.get("/get_articles_with_complaints", dependencies=[Depends(current_superuser_user)])
async def get_articles_with_complaints(
		pagination: PaginationDependency,
		order: OrderingMethods = "asc",
		session: AsyncSession = Depends(get_async_session)
):
	try:
		if order == "asc":
			order_rule = ArticleDbModel.date_of_creation.asc
		else:
			order_rule = ArticleDbModel.date_of_creation.desc

		query = (
			select(ArticleDbModel, func.count(ComplaintDbModel.id))
			.join(ComplaintDbModel)
			.group_by(ArticleDbModel.id)
			.order_by(order_rule())
			.limit(pagination.limit)
			.offset(pagination.offset)
			.options(lazyload(ArticleDbModel.creator), lazyload(ArticleDbModel.category))
		)

		result = await session.execute(query)
		result_orm = result.all()
		json_result = []
		for article, complaints_count in result_orm:
			json_result.append([ArticleRead.model_validate(article, from_attributes=True).model_dump(), complaints_count])
		json_result = json.dumps(json_result)

		return {
			"status": "success",
			"data": json_result,
			"details": None
		}

	except Exception as e:
		raise HTTPException(status_code=500, detail={
			"status": "error",
			"data": None,
			"details": str(e)
		})


@router_blog.get("/complaints", dependencies=[Depends(current_superuser_user)])
async def get_complaints(
		pagination: PaginationDependency,
		order: OrderingMethods = "asc",
		article_id: int | None = None,
		session: AsyncSession = Depends(get_async_session)
):
	try:
		if order == "asc":
			order_rule = ComplaintDbModel.date_of_creation.asc
		else:
			order_rule = ComplaintDbModel.date_of_creation.desc

		if article_id:
			query = (
				select(ComplaintDbModel)
				.where(ComplaintDbModel.article_id == article_id)
				.order_by(order_rule())
				.offset(pagination.offset)
				.limit(pagination.limit)
			)
		else:
			query = (
				select(ComplaintDbModel)
				.order_by(order_rule())
				.offset(pagination.offset)
				.limit(pagination.limit)
			)

		result = await session.execute(query)
		result_orm = result.scalars().all()
		json_result = []
		for complaint_instance in result_orm:
			json_result.append(ComplaintReadModel.model_validate(complaint_instance, from_attributes=True).model_dump())
		json_result = json.dumps(json_result)

		return {
			"status": "success",
			"data": json_result,
			"details": None
		}

	except Exception as e:
		raise HTTPException(status_code=500, detail={
			"status": "error",
			"data": None,
			"details": str(e)
		})


@router_blog.post("/add_category", dependencies=[Depends(current_active_user)])
async def create_new_category(new_category_name: str, session: AsyncSession = Depends(get_async_session)):
	"""
	This is some description
	"""
	try:
		new_category = CategoryDbModel(name=new_category_name)
		session.add(new_category)

		await session.commit()

		return {"status": "success", "data": {"id": new_category.id}}

	except IntegrityError:
		raise HTTPException(status_code=400, detail={
			"status": "error",
			"data": None,
			"details": "A category with that name already exists!"
		})

	except Exception as e:
		raise HTTPException(status_code=500, detail={
			"status": "error",
			"data": None,
			"details": str(e)
		})


@router_blog.post("/add_article", dependencies=[Depends(current_active_user)])
async def create_new_article(
		new_article_data: ArticleCreate,
		session: AsyncSession = Depends(get_async_session),
		user: UserDbModel = Depends(current_user)
):
	"""
	This is some description
	"""
	try:
		new_article = ArticleDbModel(**new_article_data.dict(), user_id=user.id)
		session.add(new_article)

		await session.commit()

		return {"status": "success", "data": {"id": new_article.id}}

	except IntegrityError as e:
		raise HTTPException(status_code=400, detail={
			"status": "error",
			"data": None,
			"details": str(e)
		})

	except Exception as e:
		raise HTTPException(status_code=500, detail={
			"status": "error",
			"data": None,
			"details": str(e)
		})


@router_blog.post("/add_comment", dependencies=[Depends(current_active_user)])
async def create_new_comment(
		new_comment_data: CommentCreate,
		session: AsyncSession = Depends(get_async_session),
		user: UserDbModel = Depends(current_user)
):
	"""
	This is some description
	"""

	try:
		new_comment = CommentDbModel(**new_comment_data.dict(), user_id=user.id)
		session.add(new_comment)

		await session.commit()

		return {"status": "success", "data": {"id": new_comment.id}}

	except IntegrityError as e:
		raise HTTPException(status_code=400, detail={
			"status": "error",
			"data": None,
			"details": str(e)
		})

	except Exception as e:
		raise HTTPException(status_code=500, detail={
			"status": "error",
			"data": None,
			"details": str(e)
		})


@router_blog.post("/add_complaint", dependencies=[Depends(current_active_user)])
async def create_new_complaint(
		new_complaint_data: ComplaintCreateModel,
		session: AsyncSession = Depends(get_async_session),
		user: UserDbModel = Depends(current_user)
):
	"""
	This is some description
	"""

	try:
		new_complaint = ComplaintDbModel(**new_complaint_data.dict(), user_id=user.id)
		session.add(new_complaint)

		await session.commit()

		return {"status": "success", "data": {"id": new_complaint.id}}

	except IntegrityError as e:
		raise HTTPException(status_code=400, detail={
			"status": "error",
			"data": None,
			"details": str(e)
		})

	except Exception as e:
		raise HTTPException(status_code=500, detail={
			"status": "error",
			"data": None,
			"details": str(e)
		})


@router_blog.delete("/delete_article", dependencies=[Depends(current_active_user)])
async def delete_article(
		article_id: int,
		session: AsyncSession = Depends(get_async_session),
		user: UserDbModel = Depends(current_user)
):
	"""
	This is some description
	"""

	try:
		query = (
			select(ArticleDbModel)
			.filter_by(id=article_id)
		)

		result = await session.execute(query)
		result_orm = result.scalars().all()
		article = result_orm[0]

		if article.user_id == user.id or user.is_superuser:
			await session.delete(article)
			await session.commit()
		else:
			raise AccessForbiddenException("custom")

	except AccessForbiddenException:
		raise HTTPException(status_code=403, detail={
				"status": "error",
				"data": None,
				"details": "Articles can only be deleted by their creator or the admin."
		})

	except IndexError as e:
		raise HTTPException(status_code=400, detail={
			"status": "error",
			"data": None,
			"details": "There are no articles with this id."
		})

	except Exception as e:
		raise HTTPException(status_code=500, detail={
			"status": "error",
			"data": None,
			"details": str(e)
		})


@router_blog.delete("/delete_comment", dependencies=[Depends(current_superuser_user)])
async def delete_comment(comment_id: int, session: AsyncSession = Depends(get_async_session)):
	"""
	This is some description
	"""

	try:
		query = (
			select(CommentDbModel)
			.filter_by(id=comment_id)
		)

		result = await session.execute(query)
		result_orm = result.scalars().all()
		article = result_orm[0]

		await session.delete(article)
		await session.commit()

	except IndexError as e:
		raise HTTPException(status_code=400, detail={
			"status": "error",
			"data": None,
			"details": "There are no comment with this id."
		})

	except Exception as e:
		raise HTTPException(status_code=500, detail={
			"status": "error",
			"data": None,
			"details": str(e)
		})


@router_blog.delete("/delete_complaint", dependencies=[Depends(current_superuser_user)], status_code=status.HTTP_204_NO_CONTENT)
async def delete_complaint(complaint_id: int, session: AsyncSession = Depends(get_async_session)):
	try:
		complaint = await session.get(ComplaintDbModel, complaint_id)
		await session.delete(complaint)
		await session.commit()

	except IndexError as e:
		raise HTTPException(status_code=400, detail={
			"status": "error",
			"data": None,
			"details": "There are no complaint with this id."
		})

	except Exception as e:
		raise HTTPException(status_code=500, detail={
			"status": "error",
			"data": None,
			"details": str(e)
		})
