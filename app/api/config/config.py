from passlib.context import CryptContext #密码加密
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "09b25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7" #密钥
ALGORITHM = "HS256" #算法
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # 访问令牌过期时间

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto") #对传入的密码加密

oauth2_schema = OAuth2PasswordBearer(tokenUrl="app/api/v1/jwt/user/token")#接受用户名和密码的token接口

#对密码进行效验
def verity_password(plain_password:str,hashed_password:str):
    ''' 对密码进行效验'''
    return pwd_context.verify(plain_password,hashed_password)

#对密码进行加密
def get_password_hash(password:str):
    return pwd_context.hash(password)