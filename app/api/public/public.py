#coding=utf-8
from datetime import datetime,timedelta
from jose import JWTError,jwt
from typing import Optional
from app.curd.User_curd import get_user_by_name,create_user
from sqlalchemy.orm import Session
from app.api.config.config import verity_password, SECRET_KEY, ALGORITHM, oauth2_schema
from app.model.test01.database import SessionLocal
from fastapi import  Depends, HTTPException,status


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

def jwt_authenticate_user(db,username:str,password:str):
    """验证用户"""
    user = get_user_by_name(db=db,name=username)

    if not user:
        return False
    elif not verity_password(plain_password=password,hashed_password=user.password):
        return False
    else:
        return user

def created_access_token(data:dict,expires_delta:Optional[timedelta]=None):
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(claims=to_encode,key=SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

async def jwt_get_current_user(db:Session=Depends(get_db),token:str=Depends(oauth2_schema)):
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not Validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token=token,key=SECRET_KEY,algorithms=[ALGORITHM])
        username =payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_name(db=db,name=username)
    if user is None:
        raise credentials_exception
    return user

