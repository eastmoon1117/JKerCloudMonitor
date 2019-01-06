#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db
from datetime import datetime
import time


class Income(db.EmbeddedDocument):
    # id
    # income_id = db.IntField(unique=True)
    # 总产币
    total_income = db.StringField()
    # 已提取币
    total_outcome = db.StringField()
    # 昨日收入
    last_income = db.StringField()
    # 近7日收入
    income_list = db.ListField()
    # 日期
    date_list = db.ListField()
    # 当月收入
    month_income = db.StringField()
    # 创建时间
    create_time = db.FloatField(default=time.mktime(datetime.now().timetuple()))
    # 更新时间
    update_time = db.FloatField(default=time.mktime(datetime.now().timetuple()))
    
    def __str__(self):
        return "user"
