# -*- coding: utf-8 -*-
# @Time : 2022/7/13 0013 14:26
# @Author : yuanjl
# @File : redis.py
# @Software: PyCharm
# @Title：redis配置
from app.api.config.config import *
from aioredis import create_redis_pool, Redis

async def get_redis_pool() -> Redis:
    if EVENT == "test":
        redis = await create_redis_pool(
            f"redis://:@" + testredishost + ":" + testredisport + "/" + testredisdb  + "?encoding=utf-8")
    else:
        redis = await create_redis_pool(f"redis://:@" + redishost + ":" + redisport + "/" + redisdb + "?encoding=utf-8")

    return redis
