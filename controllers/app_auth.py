#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import app
from flask import Flask, json, jsonify, request, abort
from datetime import datetime
from auth import Auth
from api_urls import AppUrls
from bean.jk_response import JKResponse
from bean.error_response import ErrResponse
from bean.auth_response import AuthResponse
from constant.code_constant import CodeConstant
from constant.auth_constant import AuthConstant
from strings.AuthStrings import AuthStrings
from config import Config

@app.route(AppUrls.API_AUTH_APP_AUTH, methods=['POST'])
def create_app_auth():
    data = request.data
    try:
        req_data = json.loads(data)
    except ValueError:
        return jsonify(ErrResponse(0, CodeConstant.code_null_param, AuthStrings.missing_param).__dict__)

    if not req_data \
            or not AuthConstant.token_app_key in req_data \
            or not AuthConstant.token_app_secret in req_data:
        return jsonify(ErrResponse(0, CodeConstant.code_null_param, AuthStrings.missing_param).__dict__)

    app_key = req_data[AuthConstant.token_app_key]
    app_secret = req_data[AuthConstant.token_app_secret]
    if app_key != Config.APP_KEY or app_secret != Config.APP_SECRET:
        return jsonify(ErrResponse(0, CodeConstant.code_err_param, AuthStrings.app_key_or_secret_error).__dict__)

    token = Auth.encode_app_token(app_key, app_secret)
    refresh_token = token

    auth_response = AuthResponse(token, refresh_token).__dict__
    response = JKResponse(1, auth_response).__dict__

    return jsonify(response)
