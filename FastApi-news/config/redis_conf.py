import json
from typing import Any

import redis.asyncio as redis

# 创建Redis的连接对象
redis_client = redis.Redis(
    host="redis",
    port=6379,
    db=0,
    decode_responses=True  # 解码响应结果(设为True可以把二进制类型转换为字符串类型)
)


# 设置 和 读取
# 读取：字符串
async def get_redis_client(key: str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败: {e}")
        return None


# 读取：列表或字典
async def get_redis_client_json(key: str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        print(f"获取JSON缓存失败: {e}")
        return None


# 设置缓存
async def set_cache(key: str, value: Any, expire: int = 3600):
    try:
        if isinstance(value, (dict, list)):
            # 转字符串再存
            value = json.dumps(value, ensure_ascii=False)    # 中文正常保存
        await redis_client.setex(key, expire, value)
        return True
    except Exception as e:
        print(f"设置缓存失败:{e}")
        return False
