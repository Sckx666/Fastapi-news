from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from config.db_conf import get_db
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse, UserUpdateRequest, UserUpdatePassword
from crud import users
from utils.response import success_response
from utils.auth import get_current_user

router = APIRouter(prefix="/api/user", tags=["users"])


@router.post("/register", summary="注册用户")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    """
    注册用户
    """
    # 思路：接收用户数据 -> 验证用户数据 -> 生成Token -> 保存用户数据 -> 返回注册结果
    existing_user = await users.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")
    user = await users.create_user(db, user_data)
    token = await users.generate_token(db, user.id)
    # return {
    #   "code": 200,
    #   "message": "注册成功",
    #   "data": {
    #     "token": token,
    #     "userInfo": {
    #       "id": user.id,
    #       "username": user.username,
    #       "bio": user.bio,
    #       "avatar": user.avatar
    #     }
    #   }
    # }
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(user))
    return success_response(message="注册成功", data=response_data)


@router.post("/login", summary="用户登录")
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 思路:验证用户是否存在 -> 验证密码 -> 生成Token -> 返回结果
    user = await users.authenticate_user(db, user_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    token = await users.generate_token(db, user.id)
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(user))
    return success_response(message="登录成功", data=response_data)


@router.get("/info", summary="获取用户信息")
async def get_user_info(user=Depends(get_current_user)):
    data = UserInfoResponse.model_validate(user)
    return success_response(message="获取用户信息成功", data=data)


@router.put("/update", summary="更新用户信息")
async def update_user_info(user_data: UserUpdateRequest,
                           user=Depends(get_current_user),
                           db: AsyncSession = Depends(get_db)):
    data = await users.update_user(db, user.username, user_data)
    return success_response(message="更新用户信息成功", data=UserInfoResponse.model_validate(data))


@router.put("/password", summary="修改用户密码")
async def update_user_password(user_data: UserUpdatePassword,
                               user=Depends(get_current_user),
                               db: AsyncSession = Depends(get_db)):
    data = await users.update_user_password(db, user, user_data)
    if not data:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="修改密码失败")
    return success_response(message="修改用户密码成功")











