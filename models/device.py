#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db
from datetime import datetime
import time

class Device(db.Document):
    # 设备号
    device_id = db.IntField(unique=True, required=True) 
    # 设备类型
    device_type = db.StringField()
    # 设备名
    device_name = db.StringField()
    # mac地址
    mac_addr = db.StringField(unique=True, required=True)
    # 是否在线
    online = db.BooleanField(default=False)
    # 最后在线时间
    last_online = db.FloatField(default=time.mktime(datetime.now().timetuple()))
    # 使用者的id
    user_id = db.IntField()
    # 定位地址
    location = db.StringField()
    # ip地址
    ip_addr = db.StringField()
    # 固件版本号
    version = db.StringField()
    # 创建时间
    create_time = db.FloatField(default=time.mktime(datetime.now().timetuple()))
    # 更新时间
    update_time = db.FloatField(default=time.mktime(datetime.now().timetuple()))
    
    def __str__(self):
        return "device"