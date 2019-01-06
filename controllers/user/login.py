# -*- coding: utf-8 -*-
from flask import Response

from app import app
from flask import Flask, json, jsonify, request, abort

from auth import Auth
from controllers.api_urls import AppUrls
from bean.error_response import ErrResponse
from constant.code_constant import CodeConstant
from constant.user_constant import UserConstant
from models.account import Account
from models.user import User
from strings.AuthStrings import AuthStrings
from strings.user_strings import UserStrings
from common.request_auth import ReqAuthCommon
from common.request_user import ReqUserCommon
from utils.user_utils import UserUtils
from datetime import datetime
import time
from bson import json_util
import sys

reload(sys)
sys.setdefaultencoding('utf8')

@app.route(AppUrls.API_USER_LOGIN, methods=['POST'])
def login():
    if not ReqAuthCommon.is_auth_ok(request):
        abort(401)

    req_data = ReqUserCommon.is_post_param_ok(request)
    if not req_data:
        return jsonify(ErrResponse(0, CodeConstant.code_null_param, AuthStrings.missing_param).__dict__)

    user = User.objects(username=req_data[UserConstant.username]).first()

    if not user:
        return jsonify(ErrResponse(0, CodeConstant.code_not_exist, UserStrings.user_not_exist).__dict__)

    if UserUtils.get_pwd(req_data[UserConstant.password]) != user.password:
        return jsonify(ErrResponse(0, CodeConstant.code_err_data, UserStrings.password_is_error).__dict__)

    account_list = []
    for i in range(len(user.accounts)):
        if isinstance(user.accounts[i], Account):
            account_list.append({
                'account_id': user.accounts[i].account_id,
                'username': user.accounts[i].username,
                'password': user.accounts[i].password,
                'user_id': user.accounts[i].user_id,
                'sessionid': user.accounts[i].sessionid,
                'phone_area': user.accounts[i].phone_area
            })

    token = Auth.encode_auth_token(user.user_id, time.mktime(datetime.now().timetuple()))
    
    out_user = User.objects.only('user_id', 'username', 'create_time', 'update_time').get(user_id=user.user_id)

    data = out_user.to_mongo()
    data['token'] = token
    data['accounts_list'] = account_list

    json_data = json_util.dumps({'code': 1, 'data': data}, ensure_ascii=False, sort_keys=True, indent=4)
    return Response(json_data, mimetype='application/json')
