# -*- coding: utf-8 -*-
from app import app
from flask import Flask, json, jsonify, request, abort
from datetime import datetime
import time
from auth import Auth
from controllers.api_urls import AppUrls
from bean.jk_response import JKResponse
from bean.error_response import ErrResponse
from bean.auth_response import AuthResponse
from constant.code_constant import CodeConstant
from constant.auth_constant import AuthConstant
from constant.device_constant import DeviceConstant
from strings.AuthStrings import AuthStrings 
from strings.device_strings import DeviceStrings 
from config import Config
from models.device import Device
from common.request_auth import ReqAuthCommon
from common.request_device import ReqDeviceCommon 

@app.route(AppUrls.API_ACCOUNT_GET_ACCOUNT, methods=['GET'])
def get_account_list():
    
    if(ReqAuthCommon.is_auth_ok(request) == False):
        abort(401)    
   
    devices = Device.objects().all()

    response = JKResponse(1, devices).__dict__
    
    return jsonify(response)

@app.route(AppUrls.API_ACCOUNT_GET_ACCOUNT, methods=['GET'])
def get_account_by_id(device_id):
    
    if(ReqAuthCommon.is_auth_ok(request) == False):
        abort(401)    
   
    devices = Device.objects(device_id=device_id).all()
    if not devices:
        return jsonify(ErrResponse(0, CodeConstant.code_no_data, DeviceStrings.device_not_exist).__dict__)

    response = JKResponse(1, devices).__dict__

    return jsonify(response)


