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
from utils.data_type_utils import DataTypeUtils

@app.route(AppUrls.API_ACCOUNT_UPDATE_ACCOUNT, methods=['POST'])
def update_account():
    
    if(ReqAuthCommon.is_auth_ok(request) == False):
        abort(401)    
   
    req_data = ReqDeviceCommon.is_patch_param_ok(request)
    if(req_data == False):
        return jsonify(ErrResponse(0, CodeConstant.code_null_param, AuthStrings.missing_param).__dict__)
        
    device_id = req_data[DeviceConstant.device_id]
    device = Device.objects(device_id=device_id).first()
    if not device:
        return jsonify(ErrResponse(0, CodeConstant.code_no_data, DeviceStrings.device_not_exist).__dict__)
    
    device_name = device.device_name
    if DeviceConstant.device_name in req_data:
        device_name = req_data[DeviceConstant.device_name]
    
    device_type = device.device_type
    if DeviceConstant.device_type in req_data:
        device_type = req_data[DeviceConstant.device_type]
    
    online = device.online
    if DeviceConstant.online in req_data:
        online = req_data[DeviceConstant.online]

    last_online = device.last_online
    if DeviceConstant.last_online in req_data:
        last_online = req_data[DeviceConstant.last_online]
   
    user_id = device.user_id
    if DeviceConstant.user_id in req_data:
        user_id = req_data[DeviceConstant.user_id]

    location = device.location
    if DeviceConstant.location in req_data:
        location = req_data[DeviceConstant.location]

    device.update(device_name=device_name,\
                  device_type=device_type,\
                  online=online,\
                  last_online=last_online,\
                  user_id=user_id,\
                  update_time=time.mktime(datetime.now().timetuple()))
    
    device = Device.objects(device_id=device_id).first()
    
    response = JKResponse(1, device).__dict__

    return jsonify(response)

