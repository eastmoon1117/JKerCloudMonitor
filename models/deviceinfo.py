#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db
from datetime import datetime
import time


class DeviceInfo(db.EmbeddedDocument):
    # 用户
    username = db.StringField()
    # 状态
    status = db.StringField()
    # 设备sn
    device_sn = db.StringField()
    # 绑定时间
    bind_time = db.IntField()
    # 设备名
    device_name = db.StringField()
    # 断开时间
    disconnect_time = db.IntField()
    # 连接时间
    connect_time = db.IntField()
    # 外网IP地址
    ip = db.StringField()
    # 内网IP地址
    lan_ip = db.StringField()
    # 固件版本
    system_version = db.StringField()
    # peerid
    peerid = db.StringField()
    # 硬盘容量
    usb_capacity = db.StringField()
    # 硬盘使用
    usb_used = db.StringField()
    # 总收入
    total_income = db.StringField()
    # 昨日收入
    last_day_income = db.StringField()
    # 可提币
    extract_coin = db.StringField()
    # 更新时间
    update_time = db.FloatField(default=time.mktime(datetime.now().timetuple()))
    
    def __str__(self):
        return "user"
