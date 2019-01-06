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
from models.device import Device
from strings.AuthStrings import AuthStrings 
from strings.device_strings import DeviceStrings 
from config import Config
from models.account import Account
from common.request_auth import ReqAuthCommon
from common.request_device import ReqDeviceCommon 

@app.route(AppUrls.API_USER_MODIFY_PASSWORD, methods=['POST'])
def modify_password():
    
    if not ReqAuthCommon.is_auth_ok(request):
        abort(401)       
   
    req_data = ReqDeviceCommon.is_post_param_ok(request)
    if not req_data:
        return jsonify(ErrResponse(0, CodeConstant.code_null_param, AuthStrings.missing_param).__dict__)
    
    # if Device.objects(mac_addr=req_data[DeviceConstant.mac_addr]):
    #     return jsonify(ErrResponse(0, CodeConstant.code_already_exist, DeviceStrings.device_is_exist).__dict__)
    #
    # count = Device.objects().all().count()+1
    # device = Device(mac_addr=req_data[DeviceConstant.mac_addr], device_id=0).save();
    # device.update(set__device_id=count)
    #
    # device_name = None
    # if DeviceConstant.device_name in req_data:
    #     device_name = req_data[DeviceConstant.device_name]
    #
    # device_type = None
    # if DeviceConstant.device_type in req_data:
    #     device_type = req_data[DeviceConstant.device_type]
    #
    # device.update(device_name=device_name, device_type=device_type, online=False)
    #
    response = JKResponse(1, Device.objects().first()).__dict__
    
    return jsonify(response)

