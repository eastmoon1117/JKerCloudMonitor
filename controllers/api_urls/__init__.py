#!/usr/bin/env python
# -*- coding: utf-8 -*-

class AppUrls:
    def __init__(self):
        pass

    # 1.APP
    # 1.1 认证
    API_AUTH_APP_AUTH = '/cloudmonitor/api/v1/auth/app_auth'

    # 2.User
    # 2.1 注册
    API_USER_REGISTER = '/cloudmonitor/api/v1/user/register'
    # 2.2 登录
    API_USER_LOGIN = '/cloudmonitor/api/v1/user/login'
    # 2.3 修改密码
    API_USER_MODIFY_PASSWORD = '/cloudmonitor/api/v1/user/modify_password'

    # 3.Account
    # 3.1 添加账号
    API_ACCOUNT_ADD_ACCOUNT = '/cloudmonitor/api/v1/account/add'
    # 3.2 获取账号
    API_ACCOUNT_GET_ACCOUNT = '/cloudmonitor/api/v1/account/{id}'
    # 3.3 更新账号
    API_ACCOUNT_UPDATE_ACCOUNT = '/cloudmonitor/api/v1/account/update'
    # 3.4 删除账号
    API_ACCOUNT_REMOVE_ACCOUNT = '/cloudmonitor/api/v1/account/remove'

    # 4 玩客云信息
    # 4.1 获取所有的设备信息
    API_DEVICE_GET_LIST = '/cloudmonitor/api/v1/device/get_device_list'
    API_DEVICE_GET_7DAYS_INCOME = '/cloudmonitor/api/v1/device/get_days_income'
    API_DEVICE_DRAW_LTK = '/cloudmonitor/api/v1/device/draw_ltk'

    # 5 链克行情
    # 5.1 获取链克行情
    API_LKT_MARKET_INFO = '/cloudmonitor/api/v1/lkt/market_info'
    # 5.2 获取BBX中LTK价格
    API_LKT_PRICE_INFO = '/cloudmonitor/api/v1/ltk/price_info'
