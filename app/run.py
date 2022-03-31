#coding=utf-8
import uvicorn as u
import time
from fastapi import FastAPI,Depends,Request
from app.api.v1 import application






app =FastAPI(
    title='FastAPI  and API Docs',
    description='FastAPI教程 接口文档',
    version='1.0.0',
    docs_url='/docs',
    # dependencies=[Depends(verify_token),Depends(verify_key)],
    redoc_url='/redocs'
)

@app.middleware('http')
async def add_process_time_header(request:Request,call_next):#call_next 将request请求做为参数
    '''中间件'''
    start_time = time.time()
    response = await call_next(request)
    processtime = time.time() - start_time
    response.headers['X-Process-Time'] = str(processtime)
    return response

app.include_router(application,prefix='/app/api/v1',tags=["FastAPI实操"])


if __name__ == '__main__':
    u.run('run:app', host='0.0.0.0', port=8081, reload=True, debug=True, workers=1)
