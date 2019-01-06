#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db
from datetime import datetime
from models.device import Device
import time

from models.income import Income
from models.deviceinfo import DeviceInfo


class Account(db.Document):
    # 用户id
    account_id = db.IntField()
    # 手机号
    username = db.StringField(unique=True, required=True)
    # 手机号
    phone = db.StringField()
    # email
    email = db.StringField()
    # 区域
    phone_area = db.StringField()
    # 密码, md5后的密码
    password = db.StringField(max_length=50, min_length=8, required=True)
    # 用户名
    nickname = db.StringField()
    # 登录类型
    loginType = db.StringField()
    # 用户id
    user_id = db.StringField()
    # 会话
    sessionid = db.StringField()
    # 创建时间
    create_time = db.FloatField(default=time.mktime(datetime.now().timetuple()))
    # 更新时间
    update_time = db.FloatField(default=time.mktime(datetime.now().timetuple()))

    # 账号列表，当前用户拥有的wky账号列表
    devices = db.ListField(db.ReferenceField(Device))
    income = db.EmbeddedDocumentField('Income')
    device_info = db.EmbeddedDocumentField('DeviceInfo')

    def __str__(self):
        pass
