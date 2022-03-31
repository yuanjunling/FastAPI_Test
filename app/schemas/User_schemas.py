#coding=utf-8
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class CreateUser(BaseModel):
    username:str
    user:str
    phone:str
    sex:str = '未知'
    password:str


class ReadUser(BaseModel):
    id:int
    username :str
    user: str
    phone: str
    sex:str
    updated_at: datetime
    cretaed_at: datetime
    class Config:
        orm_mode=True

class Token(BaseModel):
    """返回给用户的Token"""
    access_token:str
    token_type:str

class UpdateUser(BaseModel):
    username: str
    user: Optional[str]=None
    phone: Optional[str]=None
    sex: Optional[str]=None
    password:Optional[str]=None