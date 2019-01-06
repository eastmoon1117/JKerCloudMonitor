#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db
from datetime import datetime
from models.account import Account
import time


class User(db.Document):
    # 用户id
    user_id = db.IntField()
    # 手机号/email
    username = db.StringField(unique=True)
    # 密码
    password = db.StringField(max_length=50, min_length=8, required=True)
    # 用户名
    name = db.StringField(unique=True)
    # 性别
    sex = db.StringField()
    # 头像
    avatar = db.StringField()
    # 创建时间
    create_time = db.FloatField(default=time.mktime(datetime.now().timetuple()))
    # 更新时间
    update_time = db.FloatField(default=time.mktime(datetime.now().timetuple()))
    
    # 账号列表，当前用户拥有的wky账号列表
    accounts = db.ListField(db.ReferenceField(Account, reverse_delete_rule=db.CASCADE))

    def __str__(self):
        return "user"
