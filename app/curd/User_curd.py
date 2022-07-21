# coding=utf-8
from typing import List

from sqlalchemy.orm import Session

from app.api.config.config import get_password_hash
from app.model.test01 import models
from app.schemas.User_schemas import CreateUser, UpdateUser


def create_user(db: Session, user: CreateUser):
    """新建用户"""
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()  # 提交保存数据库中
    db.refresh(db_user)
    return db_user


def get_user_by_name(db: Session, name: str):
    '''根据用户名查询用户'''
    res = db.query(models.User).filter(models.User.username == name).first()
    return res


def get_user_by_phone(db: Session, phone: str):
    '''根据手机号码查询用户'''
    res = db.query(models.User).filter(models.User.phone == phone).first()
    return res


def get_user_by_names(db: Session, skip: int = 0, limit: int = 10):
    '''查询全部用户信息'''

    return db.query(models.User).offset(skip).limit(limit).all()


def user_update(db: Session, name: str, up: UpdateUser):
    '''根据用户名修改用户信息'''
    if not up.password:
        del up.password
    if not up.user:
        del up.user
    if not up.sex:
        del up.sex
    if not up.phone:
        del up.phone
    res = db.query(models.User).filter(models.User.username == name).update(up)
    db.commit()
    db.close()
    return res


def delete_user(db: Session, name: str):
    '''根据名称删除用户信息'''
    res = db.query(models.User).filter(models.User.username == name).delete()
    db.commit()
    db.close()
    return res


def upload_file(db: Session, rows, sheet):
    for r in range(2, rows + 1):
        usernameData = sheet.cell(row=r, column=1).value
        userData = sheet.cell(row=r, column=2).value
        phoneData = sheet.cell(row=r, column=3).value
        sexData = sheet.cell(row=r, column=4).value
        passwordData = sheet.cell(row=r, column=5).value
        if passwordData:
            password_hash = get_password_hash(str(passwordData))
        dataUser = models.User(username=usernameData, user=userData, phone=phoneData, sex=sexData,
                               password=password_hash)
        db.add(dataUser)
    db.commit()
    db.close()
