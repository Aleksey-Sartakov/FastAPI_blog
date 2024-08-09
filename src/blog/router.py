from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.blog.schemas import CategoryDbModelCreate
from src.database_settings import get_async_session
from src.blog.blog_models import CategoryDbModel

router = APIRouter(prefix="blog", tags=["Blog"])


@router.get("/categories")
def get_dashboard_report(session: AsyncSession = Depends(get_async_session)):
	try:
		query = select(CategoryDbModel)
		result = await session.execute(query)

		return {
			"status": "success",
			"data": result.mappings().all(),
			"details": None
		}

	except Exception as e:
		raise HTTPException(status_code=500, detail={
			"status": "error",
			"data": None,
			"details": e
		})


@router.post("/add_category")
def get_dashboard_report(new_category_name: str, session: AsyncSession = Depends(get_async_session)):
	try:
		pass

	except Exception as e:
		raise HTTPException(status_code=500, detail={
			"status": "error",
			"data": None,
			"details": e
		})