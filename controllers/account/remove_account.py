# -*- coding: utf-8 -*-
from bson import json_util
from flask import Response

from app import app
from flask import Flask, json, jsonify, request, abort
from datetime import datetime
import time

from bean.jk_response import JKResponse
from common.request_account import ReqAccountCommon
from common.request_user import ReqUserCommon
from constant.account_constant import AccountConstant
from controllers.api_urls import AppUrls
from bean.error_response import ErrResponse
from constant.code_constant import CodeConstant
from common.request_auth import ReqAuthCommon
from models.account import Account
from models.user import User
from strings.AuthStrings import AuthStrings
from strings.user_strings import UserStrings


@app.route(AppUrls.API_ACCOUNT_REMOVE_ACCOUNT, methods=['POST'])
def remove_account():
    user_id = ReqAuthCommon.is_auth_user_ok(request)
    if user_id == -1:
        abort(401)

    req_data = ReqAccountCommon.is_post_param_ok(request)
    if not req_data:
        return jsonify(ErrResponse(0, CodeConstant.code_null_param, AuthStrings.missing_param).__dict__)

    account = Account.objects(account_id=req_data[AccountConstant.account_id]).first()
    user = User.objects(user_id=req_data[AccountConstant.user_id]).first()
    if not account or not user:
        return jsonify(ErrResponse(0, CodeConstant.code_already_exist, UserStrings.user_not_exist).__dict__)

    user.accounts.remove(account)

    user.update(accounts=user.accounts,
                update_time=time.mktime(datetime.now().timetuple()))

    account.delete()

    json_data = json_util.dumps({'code': 1, 'data': {}}, ensure_ascii=False, sort_keys=True, indent=4)
    return Response(json_data, mimetype='application/json')

