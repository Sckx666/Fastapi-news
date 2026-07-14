from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from crud import news
from config.db_conf import get_db


router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("/categories", summary="获取新闻分类")
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    categories = await news.get_categories(db=db, skip=skip, limit=limit)
    return {
        "code": 200,
        "message": "获取新闻分类成功",
        "data": categories
    }


@router.get("/list", summary="获取新闻列表")
async def get_news(
        category_id: int = Query(alias="categoryId"),
        page: int = Query(default=1),
        page_size: int = Query(default=10, alias="pageSize", le=100),
        db: AsyncSession = Depends(get_db)
):
    # 思路:处理分页规则 -> 查询新闻列表 -> 计算总量 -> 计算是否还有更多
    skip = (page-1)*page_size
    news_list = await news.get_news_list(db=db, category_id=category_id, skip=skip, limit=page_size)
    total = await news.get_news_count(db=db, category_id=category_id)
    has_more = (skip+len(news_list)) < total
    return {
        "code": 200,
        "message": "获取新闻列表成功",
        "data": {
            "list": news_list,
            "total": total,
            "hasMore": has_more
        }
    }


@router.get("/detail", summary="获取新闻详情")
async def read_news_detail(news_id: int = Query(..., alias="id"), db: AsyncSession = Depends(get_db)):
    new_detail = await news.get_news_detail(db, news_id)
    if not new_detail:
        raise HTTPException(status_code=404, detail="新闻不存在")

    views = await news.increase_views(db, news_id)
    if not views:
        raise HTTPException(status_code=500, detail="增加阅读量失败:新闻不存在")

    related_news = await news.get_related_news(db, news_id, new_detail.category_id)

    return {
        "code": 200,
        "message": "获取新闻详情成功",
        "data": {
            "id": new_detail.id,
            "title": new_detail.title,
            "content": new_detail.content,
            "image": new_detail.image,
            "author": new_detail.author,
            "publishTime": new_detail.publish_time,
            "category_id": new_detail.category_id,
            "view": new_detail.views,
            "relatedNews": related_news,
        }
    }
