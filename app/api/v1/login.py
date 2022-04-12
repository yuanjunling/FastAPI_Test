
from fastapi.security import OAuth2PasswordRequestForm
from app.api.config.config import ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash
from app.api.public.public import get_db, jwt_authenticate_user, created_access_token, jwt_get_current_user
from app.curd.User_curd import get_user_by_name, get_user_by_phone, create_user
from app.model.test01.models import User
from app.schemas.User_schemas import Token, ReadUser, CreateUser
from fastapi import APIRouter, Depends, HTTPException,status,Request
from sqlalchemy.orm import Session
from app.api.v1.extensions.logger import logger
from datetime import datetime,timedelta


Login=APIRouter()


#注册用户
@Login.post('/create_user',response_model=ReadUser,summary="注册用户")
async def create_users(user:CreateUser,db:Session=Depends(get_db)):
    db_user =get_user_by_name(db=db,name=user.username) #用户名是否已存在
    db_phone = get_user_by_phone(db=db,phone=user.phone)#手机号码是否已存在
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='您输入的用户已存在')

    if db_phone:
        logger.error('您输入的手机号码已存在')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='您输入的手机号码已存在')

    try:
        user.password = get_password_hash(user.password)

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='密码加密失败')
    try:
        user = create_user(db=db, user=user)
        now_time = datetime.now()
        str_time = now_time.strftime("%Y-%m-%d %X")  # 格式化时间字符串
        logger.debug('用户{0}注册成功，注册时间:{1},日志记录'.format(user.username,str_time))
        return user
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='注册失败')
#登录获取token
@Login.post("/jwt/user/token",response_model=Token,summary="生成token")
async def login_for_access_token(request: Request,db:Session=Depends(get_db),form_data:OAuth2PasswordRequestForm = Depends()):
    user = jwt_authenticate_user(db=db,username=form_data.username,password=form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",
            headers = {"WWW-Authenticate": "Bearer"}
        )
    else:
        #token过期时间
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES * 604800)
        access_token = created_access_token(
            data={"sub":user.username},
            expires_delta=access_token_expires
        )
        useris = await request.app.state.redis.get(user.username)
        if not useris:
            await request.app.state.redis.set(user.username, access_token, expire=ACCESS_TOKEN_EXPIRE_MINUTES * 604800 )

        return {
            "access_token":access_token,
            "token_type":"bearer"
        }

@Login.put("/logout", summary="注销")
async def user_logout(request: Request, user: User = Depends(jwt_get_current_user)):
    try:
        logger.debug('用户{}，退出成功'.format(user.username))
        await request.app.state.redis.delete(user.username)
        return {
            "rode":"200",
            'message':'操作成功'
        }
    except:
        logger.error('用户退出失败')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='用户退出失败')