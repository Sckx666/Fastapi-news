from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, Select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from cache.news import get_cached_categories, set_cache_categories, get_cache_news_list, set_cache_news_list
from models.news import Category,News
from schemas.base import NewsItemBase


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    # 先尝试从缓存中获取数据
    categories = await get_cached_categories()
    if categories:
        return categories

    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all()

    # 写入缓存
    if categories:
        categories = jsonable_encoder(categories)
        await set_cache_categories(categories)

    # 返回数据
    return categories


async def get_news_list(db: AsyncSession, category_id: int, skip: int =0, limit: int =10):
    # 先尝试从缓存中获取数据
    page = skip // limit + 1
    news_list = await get_cache_news_list(category_id, page, limit)
    if news_list:
        print("成功读取")
        return [News(**item) for item in news_list]

    # 查询的是指定分类下的所有新闻
    stmt: Select = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    news_list = result.scalars().all()

    # 写入缓存
    if news_list:
        news_data = [NewsItemBase.model_validate(item).model_dump(mode="json", by_alias=False) for item in news_list]
        await set_cache_news_list(category_id, page, limit, news_data)

    # 返回数据
    return news_list


async def get_news_count(db: AsyncSession, category_id: int):
    # 查询的是指定分类下的新闻数量总量
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    count = result.scalar_one_or_none()
    return count


async def get_news_detail(db: AsyncSession, id: int):
    stmt = select(News).where(News.id == id)
    result = await db.execute(stmt)
    news_detail = result.scalar_one_or_none()
    return news_detail


async def increase_views(db: AsyncSession, id: int):
    stmt = update(News).where(News.id == id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()

    # 更新 -> 检查数据库是否真的更新了 -> 命中返回true，没有命中返回false
    return result.rowcount > 0


async def get_related_news(db: AsyncSession, id: int, category_id: int, limit: int = 5):
    stmt = select(News).where(
        News.id != id,
        News.category_id == category_id
    ).order_by(
        News.views.desc(),
        News.publish_time.desc()
    ).limit(limit)
    result = await db.execute(stmt)
    related_news = result.scalars().all()
    return [{
        "id": new_detail.id,
        "title": new_detail.title,
        "content": new_detail.content,
        "image": new_detail.image,
        "author": new_detail.author,
        "publishTime": new_detail.publish_time,
        "category_id": new_detail.category_id,
        "view": new_detail.views,
    } for new_detail in related_news]






