#coding=utf-8
from datetime import datetime
from typing import Optional

from fastapi import Body
from pydantic import BaseModel

class JiekouCanshuJieshi(BaseModel):
    para1: str
    para2: int
    para3: Optional[str] = None
    para4: Optional[str] = '自己添加'
    para5: Optional[int] = 110



