# -*- coding: utf-8 -*-
from bson import json_util
from flask import Response

from app import app
from flask import Flask, json, jsonify, request, abort

from bean.jk_response import JKResponse
from common.request_device import ReqDeviceCommon
from constant.account_constant import AccountConstant
from constant.device_constant import DeviceConstant
from controllers.api_urls import AppUrls
from bean.error_response import ErrResponse
from constant.code_constant import CodeConstant
from models.account import Account
from models.user import User
from strings.device_strings import DeviceStrings
from strings.user_strings import UserStrings
from common.request_auth import ReqAuthCommon
from strings.AuthStrings import AuthStrings
import sys
from datetime import datetime
import time

from wky.wky_interface import WKYInterface

reload(sys)
sys.setdefaultencoding('utf8')


@app.route(AppUrls.API_DEVICE_DRAW_LTK, methods=['POST'])
def draw_ltk():
    user_id = ReqAuthCommon.is_auth_user_ok(request)
    if user_id == -1:
        abort(401)

    req_data = ReqDeviceCommon.is_post_param_with_wkb_ok(request)
    if not req_data:
        return jsonify(ErrResponse(0, CodeConstant.code_null_param, AuthStrings.missing_param).__dict__)

    account = Account.objects(account_id=req_data[DeviceConstant.account_id]).first()
    user = User.objects(user_id=req_data[DeviceConstant.user_id]).first()
    if not account or not user:
        return jsonify(ErrResponse(0, CodeConstant.code_already_exist, UserStrings.user_not_exist).__dict__)

    json_draw_wkb = getWKYIncome(account, req_data[DeviceConstant.draw_wkb])

    if 'iRet' not in json_draw_wkb:
        return jsonify(ErrResponse(0, CodeConstant.code_err_data, DeviceStrings.device_draw_failed).__dict__)

    if json_draw_wkb['iRet'] != 0:
        return jsonify(ErrResponse(0, CodeConstant.code_err_data, json_draw_wkb['sMsg']).__dict__)

    json_data = json_util.dumps({'code': 1, 'data': {}}, ensure_ascii=False, sort_keys=True, indent=4)
    return Response(json_data, mimetype='application/json')


def getWKYIncome(account, draw_wkb):

    wky = WKYInterface()

    data_draw_wkb = wky.drawLTK(account.sessionid, account.user_id, account.device_info.peerid, draw_wkb)

    json_draw_wkb = json.loads(data_draw_wkb)

    return json_draw_wkb
