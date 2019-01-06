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
from models.income import Income
from models.user import User
from strings.user_strings import UserStrings
from common.request_auth import ReqAuthCommon
import sys
from datetime import datetime
import time

from wky.wky_interface import WKYInterface

reload(sys)
sys.setdefaultencoding('utf8')


@app.route(AppUrls.API_DEVICE_GET_7DAYS_INCOME, methods=['POST'])
def get_device_7days_income_list_by_user_id():
    user_id = ReqAuthCommon.is_auth_user_ok(request)
    if user_id == -1:
        abort(401)

    req_data = ReqDeviceCommon.is_post_param_ok(request)
    if not req_data:
        return jsonify(ErrResponse(0, CodeConstant.code_null_param, Auth.missing_param).__dict__)

    user = User.objects(user_id=req_data[DeviceConstant.user_id]).first()

    if not user:
        return jsonify(ErrResponse(0, CodeConstant.code_not_exist, UserStrings.user_not_exist).__dict__)

    income7Days = ['0', '0', '0', '0', '0', '0', '0']
    data7Days = ['', '', '', '', '', '', '']
    total_income = 0.0
    device_num = 0
    current_month_income = 0.0
    last_income = 0.0
    total_outcome = 0.0

    if len(user.accounts) == 0:
        json_data = json_util.dumps({'code': 1, 'data': {}}, ensure_ascii=False, sort_keys=True, indent=4)
        return Response(json_data, mimetype='application/json')

    for i in range(len(user.accounts)):
        if isinstance(user.accounts[i], Account):

            if user.accounts[i].income is None:
                getWKYIncome(user.accounts[i])
            else: 
                time_income = time.localtime(user.accounts[i].income.update_time)
                time_now = time.localtime(time.mktime(datetime.now().timetuple()))

                if user.accounts[i].income is None \
                        or time_now.tm_year > time_income.tm_year \
                        or time_now.tm_mon > time_income.tm_mon \
                        or time_now.tm_mday > time_income.tm_mday:
                    getWKYIncome(user.accounts[i])

            total_income += float(user.accounts[i].income.total_income)
            total_outcome += float(user.accounts[i].income.total_outcome)
            last_income += float(user.accounts[i].income.last_income)
            current_month_income += float(user.accounts[i].income.month_income)
            device_num += 1

            for k in range(7):
                data7Days[k] = user.accounts[i].income.date_list[k]
                income7Days[k] = str(round(float(income7Days[k]) + float(user.accounts[i].income.income_list[k]), 4))

    max_num = float(income7Days[0])
    min_num = float(income7Days[0])
    for k in range(len(income7Days)):
        if max_num < float(income7Days[k]):
            max_num = float(income7Days[k])
        if min_num > float(income7Days[k]):
            min_num = float(income7Days[k])

    if device_num == 0:
        device_num = 1

    out_data = {
        'last_income': str(round(last_income, 4)),
        'last_average': str(round(last_income / device_num, 4)),
        'current_month_income': str(round(current_month_income, 4)),
        'total_income': str(round(total_income, 4)),
        'total_outcome': str(round(total_outcome, 4)),
        'remainder_coin': str(round(total_income - total_outcome, 4)),
        'seven_days_date': data7Days,
        'seven_days_income': income7Days,
        'chart_min': min_num - 0.1,
        'chart_max': max_num + 0.1
    }

    json_data = json_util.dumps({'code': 1, 'data': out_data}, ensure_ascii=False, sort_keys=True, indent=4)
    return Response(json_data, mimetype='application/json')


def getWKYIncome(account):
    check_and_update_account(account.account_id)

    wky = WKYInterface()

    month_income = wky.getMonthIncome('0', account.sessionid, account.user_id)
    json_month_income = json.loads(month_income)

    coin_info = wky.getCoinInfo(account.sessionid, account.user_id)
    json_coin_info = json.loads(coin_info)

    if 'iRet' not in json_month_income:
        return
    if json_month_income['iRet'] != 0:
        return
    if 'iRet' not in json_coin_info:
        return
    if json_coin_info['iRet'] != 0:
        return

    data_month_income = json_month_income['data']
    data_coin_info = json_coin_info['data']

    if 'month' in data_month_income and data_month_income['month'] != "":
        last_month_income = wky.getMonthIncome(data_month_income['month'], account.sessionid,
                                               account.user_id)
        json_last_month_income = json.loads(last_month_income)

        if 'iRet' not in json_last_month_income:
            return

    if json_last_month_income['iRet'] != 0:
        return

    data_last_month_income = json_last_month_income['data']
    print data_last_month_income

    total_income = str(data_month_income['totalIncome'])
    total_outcome = str(data_coin_info['totalOutcome'])

    current_month_income = 0
    date_list = []
    income_list = []

    if len(data_month_income['incomeArr']) > 0:
        last_income = data_month_income['incomeArr'][0]['num']
        for kk in range(len(data_month_income['incomeArr'])):
            current_month_income += float(data_month_income['incomeArr'][kk]['num'])
    else:
        last_income = data_last_month_income['incomeArr'][0]['num']

    month_income = str(current_month_income)

    for k in range(7):
        current_len = len(data_month_income['incomeArr'])
        if k < current_len:
            date_list.append(data_month_income['incomeArr'][k]['date'][4:])
            income_list.append(data_month_income['incomeArr'][k]['num'])
        else:
            date_list.append(data_last_month_income['incomeArr'][k-current_len]['date'][4:])
            income_list.append(data_last_month_income['incomeArr'][k-current_len]['num'])

    income_list.reverse()
    date_list.reverse()

    income = Income(total_income=total_income,
                    total_outcome=total_outcome,
                    last_income=last_income,
                    month_income=month_income,
                    date_list=date_list,
                    income_list=income_list,
                    update_time=time.mktime(datetime.now().timetuple()))
    account = Account.objects(account_id=account.account_id).first()
    if account is None:
        return

    account.update(income=income,
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
