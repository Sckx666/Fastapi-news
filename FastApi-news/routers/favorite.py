from fastapi import APIRouter, Depends, HTTPException
from fastapi import Query
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from models.users import User
from schemas.favorite import FavoriteCheckResponse, FavoriteAddRequest, FavoriteListResponse
from utils.auth import get_current_user
from utils.response import success_response
from crud import favorite

router = APIRouter(prefix="/api/favorite",tags=["favorite"])


@router.get("/check", summary="检查收藏状态")
async def check_favorite(
    news_id: int = Query(..., alias="newsId"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    is_favorite = await favorite.is_news_favorite(db, user.id, news_id)
    return success_response(message="检查收藏状态成功", data=FavoriteCheckResponse(is_favorite=is_favorite))


@router.post("/add", summary="添加收藏")
async def add_favorite(
        data: FavoriteAddRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    result = await favorite.add_news_favorite(db, user.id, data.news_id)
    return success_response(message="添加收藏成功", data=result)


@router.delete("/remove", summary="取消收藏")
async def remove_favorite(
        news_id: int = Query(..., alias="newsId"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    result = await favorite.delete_news_favorite(db, user.id, news_id)
    if not result:
        raise HTTPException(status_code=404, detail="取消收藏失败")
    return success_response("取消收藏他成功")


# 获取收藏列表
@router.get("/list", summary="获取收藏列表")
async def get_favorite_list(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    rows, total = await favorite.get_favorite_list(db, user.id, page, page_size)
    favorite_list = [{
        **news.__dict__,
        "favorite_time": favorite_time,
        "favorite_id": favorite_id
    } for news, favorite_time, favorite_id in rows]
    has_more = total > page * page_size

    data = FavoriteListResponse(list=favorite_list, total=total, has_more=has_more)
    return success_response(message="获取收藏列表成功", data=data)


@router.delete("/clear", summary="清空收藏")
async def clear_favorite(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    count = await favorite.clear_favorite_list(db, user.id)
    return success_response(message=f"清空收藏成功,清空{count}条新闻")