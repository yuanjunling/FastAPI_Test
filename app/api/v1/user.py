#coding=utf-8
from typing import List

from app.File.file_data.user_data import user_result
from app.api.config.config import get_password_hash
from app.api.public.public import get_db, jwt_get_current_user, \
    download_file, saveRaw, excel_data_uploading_db
from app.curd.User_curd import get_user_by_name, user_update, delete_user, get_user_by_names
from app.model.test01.database import engine, Base
from app.schemas.User_schemas import ReadUser,  UpdateUser
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from datetime import datetime
from app.api.v1.extensions.logger import logger




application=APIRouter(dependencies=[Depends(jwt_get_current_user)])
Base.metadata.create_all(bind=engine)

#获取单个用户信息
@application.get("/jwt/users/me",response_model=ReadUser,summary='获取用户信息')
async def jwt_read_users_me(username:str,db:Session=Depends(get_db)):
    db_user = get_user_by_name(db=db, name=username)
    # logger.info('这是取单个用户信息接口：username={},当前时间戳为：{tiems}', username, tiems=time.time())
    # my_function(0, 0, 0)
    if db_user is None :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='您输入的数据有误')
    else:
        return db_user

#获取全部用户信息
@application.get("/jwt/users/mes",response_model=List[ReadUser],summary='获取全部用户信息')
async def jwt_read_users_mes(db:Session=Depends(get_db),skip:int=0,limit:int=10):
    db_user = get_user_by_names(db=db,skip=skip,limit=limit)
    return db_user

#修改用户信息
@application.put('/jwt/users/put',summary='修改用户信息')
async def user_updates(user_form:UpdateUser,db:Session=Depends(get_db)):
    db_user = get_user_by_name(db=db, name=user_form.username)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='您输入的用户不存在')
    try:
        if user_form.password:
            user_form.password = get_password_hash(user_form.password)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='密码加密失败')

    try:
        user_update(db=db,name=user_form.username,up=user_form)
        return {"Message":"修改用户信息成功"}
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='修改用户信息失败')

#删除用户信息
@application.delete('/jwt/user/delete',summary='删除用户信息',description='接口1描述')
async def get_user_delete(
        username:str,
        db:Session=Depends(get_db)):
    db_user = get_user_by_name(db=db, name=username)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='您输入的用户不存在')
    else:
        try:
            delete_user(db=db,name=username)
            return {"Message":"删除用户信息成功"}
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='删除用户信息失败')

@application.get("/jwt/user/download", summary="下载文件")
async def download_files():
    try:
        file=await download_file(user_result)
        return {
            "rode": "200",
            'message': '操作成功',
            'filepath':file.path,
            'filename':file.filename
        }
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='文件下载失败')

@application.post("/upload_files",summary='上传数据')
async def upload_files(db:Session=Depends(get_db),files:UploadFile=File(...)):
    contents = await files.read()
    file_name_data=await saveRaw(contents, files.filename)
    now_time = datetime.now()
    str_time = now_time.strftime("%Y-%m-%d %X")  # 格式化时间字符串
    result=await excel_data_uploading_db(file_name_data=file_name_data,str_time=str_time,db=db)
    return result


