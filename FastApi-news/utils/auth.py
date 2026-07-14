# 整合 Token 查询用户，返回用户
from fastapi import Header, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_conf import get_db
from crud import users


async def get_current_user(
        authorization: str = Security(APIKeyHeader(name="Authorization")),
        db: AsyncSession = Depends(get_db)
):
    print(authorization)
    token = authorization.replace("Bearer ", "")
    user = await users.get_user_by_token(db, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token 无效或已经过期")

    return user
