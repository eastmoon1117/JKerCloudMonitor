# -*- coding: utf-8 -*-
from flask import Response

from app import app
from flask import Flask, json, jsonify, request, abort

from auth import Auth
from common.request_user import ReqUserCommon
from constant.user_constant import UserConstant
from controllers.api_urls import AppUrls
from bean.error_response import ErrResponse
from constant.code_constant import CodeConstant
from models.user import User
from strings.AuthStrings import AuthStrings
from common.request_auth import ReqAuthCommon
from strings.user_strings import UserStrings
from utils.user_utils import UserUtils

from datetime import datetime
import time
from bson import json_util
import sys

reload(sys)
sys.setdefaultencoding('utf8')

@app.route(AppUrls.API_USER_REGISTER, methods=['POST'])
def register():
    if not ReqAuthCommon.is_auth_ok(request):
        abort(401)

    req_data = ReqUserCommon.is_post_param_ok(request)
    if not req_data:
        return jsonify(ErrResponse(0, CodeConstant.code_null_param, AuthStrings.missing_param).__dict__)

    if User.objects(username=req_data[UserConstant.username]):
        return jsonify(ErrResponse(0, CodeConstant.code_already_exist, UserStrings.user_is_exist).__dict__)

    count = User.objects().all().count() + 1
    user = User(username=req_data[UserConstant.username],
                name=req_data[UserConstant.username],
                password=UserUtils.get_pwd(req_data[UserConstant.password]),
                user_id=count
                ).save()
    user.update(set__user_id=count)

    out_user = User.objects.only('user_id', 'username', 'create_time', 'update_time').get(user_id=count)
    token = Auth.encode_auth_token(user.user_id, time.mktime(datetime.now().timetuple()))

    data = out_user.to_mongo()
    data['token'] = token

    json_data = json_util.dumps({'code': 1, 'data': data}, ensure_ascii=False, sort_keys=True, indent=4)
    return Response(json_data, mimetype='application/json')

