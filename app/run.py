#coding=utf-8
import uvicorn as u
import time
from fastapi import FastAPI,Depends,Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from app.api.config.config import *
from app.api.v1 import application,Login
from aioredis import create_redis_pool, Redis






app =FastAPI(
    title='FastAPI  and API Docs',
    description='FastAPI教程 接口文档',
    version='1.0.0',
    docs_url='/docs',
    # dependencies=[Depends(verify_token),Depends(verify_key)],
    redoc_url='/redocs'
)

async def get_redis_pool() -> Redis:

    if EVENT=="test":
        redis = await create_redis_pool(f"redis://:@" + testredishost + ":" + testredisport + "/" + testredisdb + "?encoding=utf-8")
    else:
        redis = await create_redis_pool(f"redis://:@" + redishost + ":" + redisport + "/" + redisdb + "?encoding=utf-8")

    return redis

@app.on_event("startup")
async def startup_event():
    app.state.redis = await get_redis_pool()


@app.on_event("shutdown")
async def shutdown_event():
    app.state.redis.close()
    await app.state.redis.wait_closed()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        content=jsonable_encoder({"message": exc.errors(), "code": 421}),
    )

@app.middleware('http')
async def add_process_time_header(request:Request,call_next):#call_next 将request请求做为参数
    '''中间件'''
    start_time = time.time()
    response = await call_next(request)
    processtime = time.time() - start_time
    response.headers['X-Process-Time'] = str(processtime)
    return response
app.include_router(Login,prefix='/api/v1/login',tags=["登录注册"])
app.include_router(application,prefix='/api/v1/user',tags=["用户操作"])



if __name__ == '__main__':
    u.run('run:app', host='0.0.0.0', port=8081, reload=True, debug=True, workers=1)
