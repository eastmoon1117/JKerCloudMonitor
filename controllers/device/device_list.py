# -*- coding: utf-8 -*-
from bson import json_util
from flask import Response

from app import app
from flask import Flask, json, jsonify, request, abort

from auth import Auth
from common.request_device import ReqDeviceCommon
from constant.device_constant import DeviceConstant
from controllers.api_urls import AppUrls
from bean.error_response import ErrResponse
from constant.code_constant import CodeConstant
from models.account import Account
from models.deviceinfo import DeviceInfo
from models.user import User
from strings.user_strings import UserStrings
from common.request_auth import ReqAuthCommon
import sys
from datetime import datetime
import time

from wky.wky_interface import WKYInterface

reload(sys)
sys.setdefaultencoding('utf8')


@app.route(AppUrls.API_DEVICE_GET_LIST, methods=['POST'])
def get_device_list_by_user_id():
    user_id = ReqAuthCommon.is_auth_user_ok(request)
    if user_id == -1:
        abort(401)

    req_data = ReqDeviceCommon.is_post_param_ok(request)
    if not req_data:
        return jsonify(ErrResponse(0, CodeConstant.code_null_param, Auth.missing_param).__dict__)

    user = User.objects(user_id=req_data[DeviceConstant.user_id]).first()

    if not user:
        return jsonify(ErrResponse(0, CodeConstant.code_not_exist, UserStrings.user_not_exist).__dict__)

    device_list = []
    online_device_num = 0
    offline_device_num = 0
    total_income = 0

    if len(user.accounts) == 0:
        json_data = json_util.dumps({'code': 1, 'data': {}}, ensure_ascii=False, sort_keys=True, indent=4)
        return Response(json_data, mimetype='application/json')

    for i in range(len(user.accounts)):
        if isinstance(user.accounts[i], Account):

            if user.accounts[i].device_info is None:
                getWKYDeviceInfo(user.accounts[i])
            else:
                time_device_info = time.localtime(user.accounts[i].device_info.update_time)
                time_now = time.localtime(time.mktime(datetime.now().timetuple()))

                if user.accounts[i].device_info is None \
                        or time_now.tm_year > time_device_info.tm_year \
                        or time_now.tm_mon > time_device_info.tm_mon \
                        or time_now.tm_mday > time_device_info.tm_mday:
                    getWKYDeviceInfo(user.accounts[i])

            total_income += float(user.accounts[i].device_info.last_day_income)
            if user.accounts[i].device_info.status == "online":
                online_device_num += 1
            else:
                offline_device_num += 1

            device_list.append({
                'account_id': user.accounts[i].account_id,
                'username': user.accounts[i].username,
                'status': user.accounts[i].device_info.status,
                'bind_time': user.accounts[i].device_info.bind_time,
                'device_sn': user.accounts[i].device_info.device_sn,
                'device_name': user.accounts[i].device_info.device_name,
                'disconnect_time': user.accounts[i].device_info.disconnect_time,
                'ip': user.accounts[i].device_info.ip,
                'system_version': user.accounts[i].device_info.system_version,
                'lan_ip': user.accounts[i].device_info.lan_ip,
                'peerid': user.accounts[i].device_info.peerid,
                'connect_time': user.accounts[i].device_info.connect_time,
                'usb_capacity': user.accounts[i].device_info.usb_capacity,
                'usb_used': user.accounts[i].device_info.usb_used,
                'totalIncome': user.accounts[i].device_info.total_income,
                'last_day_income': user.accounts[i].device_info.last_day_income,
                'extract_coin': user.accounts[i].device_info.extract_coin,
                'update_time': time.strftime("%Y-%m-%d %H:%M:%S", time_device_info)
            })

    out_data = {
        'device_list': device_list,
        'online_num': online_device_num,
        'offline_num': offline_device_num,
        'total_income': round(total_income, 3),
    }

    json_data = json_util.dumps({'code': 1, 'data': out_data}, ensure_ascii=False, sort_keys=True, indent=4)
    return Response(json_data, mimetype='application/json')


def getWKYDeviceInfo(account):
    check_and_update_account(account.account_id)

    wky = WKYInterface()

    device_info = wky.getDeviceInfo(account.sessionid, account.user_id)
    json_device_info = json.loads(device_info)

    month_income = wky.getMonthIncome('0', account.sessionid, account.user_id)
    json_month_income = json.loads(month_income)

    coin_info = wky.getCoinInfo(account.sessionid, account.user_id)
    json_coin_info = json.loads(coin_info)

    if 'result' not in json_device_info:
        return
    if json_device_info['rtn'] != 0:
        return

    if 'iRet' not in json_month_income:
        return
    if json_month_income['iRet'] != 0:
        return
    if 'iRet' not in json_coin_info:
        return
    if json_coin_info['iRet'] != 0:
        return

    data_device_info = json_device_info['result'][1]['devices'][0]
    data_month_income = json_month_income['data']
    data_coin_info = json_coin_info['data']

    device_usb_info = wky.getDeviceUsbInfo(account.sessionid, account.user_id,
                                           data_device_info['device_id'])
    json_device_usb_info = json.loads(device_usb_info)

    usb_capacity = 0
    usb_used = 0
    if 'result' in json_device_usb_info and json_device_usb_info['rtn'] == 0:
        for i in range(len(json_device_usb_info['result'][1]['partitions'])):
            data_device_usb_info = json_device_usb_info['result'][1]['partitions'][i]
            usb_capacity += float(data_device_usb_info['capacity'])
            usb_used += float(data_device_usb_info['used'])

    if 'month' in data_month_income and data_month_income['month'] != "":
        last_month_income = wky.getMonthIncome(data_month_income['month'], account.sessionid,
                                               account.user_id)
        json_last_month_income = json.loads(last_month_income)

        if 'iRet' not in json_last_month_income:
            return

    if json_last_month_income['iRet'] != 0:
        return

    data_last_month_income = json_last_month_income['data']

    total_income = str(data_month_income['totalIncome'])
    extract_coin = str(float(total_income) - float(data_coin_info['totalOutcome']))

    if len(data_month_income['incomeArr']) > 0:
        last_income = data_month_income['incomeArr'][0]['num']
    else:
        last_income = data_last_month_income['incomeArr'][0]['num']

    account = Account.objects(account_id=account.account_id).first()
    if account is None:
        return

    device_info = DeviceInfo(account.device_info)

    device_info.username = account.username

    device_info.status = data_device_info['status']
    device_info.bind_time = data_device_info['bind_time']
    device_info.device_sn = data_device_info['device_sn']
    device_info.device_name = data_device_info['device_name']
    device_info.disconnect_time = data_device_info['disconnect_time']
    device_info.ip = data_device_info['ip']
    device_info.system_version = data_device_info['system_version']
    device_info.lan_ip = data_device_info['lan_ip']
    device_info.peerid = data_device_info['peerid']
    device_info.connect_time = data_device_info['connect_time']

    device_info.usb_capacity = str(round(usb_capacity / 1024 / 1024 / 1024, 2)) + 'GB'
    device_info.usb_used = str(round(usb_used / 1024 / 1024 / 1024, 2)) + 'GB'
    device_info.total_income = total_income
    device_info.last_day_income = last_income
    device_info.extract_coin = extract_coin
    device_info.update_time = time.mktime(datetime.now().timetuple())

    account.update(device_info=device_info,
                   update_time=time.mktime(datetime.now().timetuple()))


def check_and_update_account(account_id):
    wky = WKYInterface()

    account = Account.objects(account_id=account_id).first()
    if account is None:
        return

    month_income = wky.getMonthIncome('0', account.sessionid, account.user_id)
    json_month_income = json.loads(month_income)

    if 'iRet' in json_month_income and json_month_income['iRet'] == 0:
        return

    wky_account = wky.login(account.username, account.password, account.phone_area)
    if wky_account.user_id is None or wky_account.sessionid is None:
        return jsonify(ErrResponse(0, CodeConstant.code_err_bind, UserStrings.bind_error).__dict__)

    account.update(sessionid=wky_account.sessionid,
                   update_time=time.mktime(datetime.now().timetuple()))
