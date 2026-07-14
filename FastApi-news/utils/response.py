from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


# 封装响应内容
# 目标：把任何的Fastapi、Pydantic、ORM对象 都要正常响应
def success_response(message: str, data=None):
    content = {
        "code": 200,
        "message": message,
        "data": data
    }
    return content
