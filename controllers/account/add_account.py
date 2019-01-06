# -*- coding: utf-8 -*-
from app import app
from flask import Flask, json, jsonify, request, abort

from common.request_user import ReqUserCommon
from constant.user_constant import UserConstant
from controllers.api_urls import AppUrls
from bean.jk_response import JKResponse
from bean.error_response import ErrResponse
from constant.code_constant import CodeConstant
from models.account import Account
from models.user import User
from strings.AuthStrings import AuthStrings
from common.request_auth import ReqAuthCommon
from strings.user_strings import UserStrings
from utils.user_utils import UserUtils
from wky.wky_interface import WKYInterface
from datetime import datetime
import time


@app.route(AppUrls.API_ACCOUNT_ADD_ACCOUNT, methods=['POST'])
def create_account():
    user_id = ReqAuthCommon.is_auth_user_ok(request)
    if user_id <= 0:
        abort(401)

    req_data = ReqUserCommon.is_post_param_ok(request)
    if not req_data:
        return jsonify(ErrResponse(0, CodeConstant.code_null_param, AuthStrings.missing_param).__dict__)

    if Account.objects(username=req_data[UserConstant.username]):
        return jsonify(ErrResponse(0, CodeConstant.code_already_exist, UserStrings.account_exist).__dict__)

    username = req_data[UserConstant.username]
    password = UserUtils.get_pwd(req_data[UserConstant.password])
    phone_area = UserUtils.get_phone_area_by_name(username)

    wky = WKYInterface()
    account = wky.login(username, password, phone_area)
    if account.user_id is None or account.sessionid is None:
        return jsonify(ErrResponse(0, CodeConstant.code_err_bind, UserStrings.bind_error).__dict__)

    count = Account.objects().all().count() + 1

    account.phone_area = phone_area
    account.username = username
    account.password = password
    account.account_id = 0
    account.save()
    account.update(set__account_id=count)

    print 'user_id:'+str(user_id)

    user = User.objects(user_id=user_id).first()
    user.accounts.append(account)
    user.update(accounts=user.accounts,
                update_time=time.mktime(datetime.now().timetuple()))

    response = JKResponse(1, account).__dict__

    return jsonify(response)
