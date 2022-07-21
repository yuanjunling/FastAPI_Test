# coding=utf-8
import os.path
import sys
from app.model.test01.redis import get_redis_pool
sys.path.append('/FastAPI_Yuan')
import uvicorn as u
import time
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from app.api.v1 import application, Login
from core import Events

app = FastAPI(
    title='FastAPI  and API Docs',
    description='FastAPI教程 接口文档',
    version='1.0.0',
    docs_url='/docs',
    # dependencies=[Depends(verify_token),Depends(verify_key)],
    redoc_url='/redocs'
)



#redis启动
@app.on_event("startup")
async def startup_event():
    app.state.redis = await get_redis_pool()

#redis关闭
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
async def add_process_time_header(request: Request, call_next):  # call_next 将request请求做为参数
    '''中间件'''
    start_time = time.time()
    response = await call_next(request)
    processtime = time.time() - start_time
    response.headers['X-Process-Time'] = str(processtime)
    return response


# 事件监听
app.add_event_handler('startup', Events.startup(app))
app.add_event_handler('shutdown', Events.stopping(app))

# 绑定静态资源
app.mount('/static', StaticFiles(directory=os.path.join(os.getcwd(), 'static')))

# 注册路由
app.include_router(Login, prefix='/api/v1/login', tags=["登录注册"])
app.include_router(application, prefix='/api/v1/user', tags=["用户操作"])

if __name__ == '__main__':
    u.run('run:app', host='0.0.0.0', port=8081, reload=True, debug=True, workers=1)
