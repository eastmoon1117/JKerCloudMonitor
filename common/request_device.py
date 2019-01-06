# -*- coding: utf-8 -*-
import json
from constant.device_constant import DeviceConstant
from utils.device_utils import DeviceUtils
from utils.data_type_utils import DataTypeUtils
import types

class ReqDeviceCommon:
    @staticmethod
    def is_param_ok(request):
        data = request.data
        try:  
            req_data = json.loads(data)
        except ValueError:  
            return False

        if not req_data \
            or not DeviceConstant.mac_addr in req_data:
            return False 
         
        return req_data
    
    @staticmethod
    def is_patch_param_ok(request):
        data = request.data
        try:  
            req_data = json.loads(data)
        except ValueError:  
            return False

        if not req_data \
            or not DeviceConstant.device_id in req_data:
            return False 
                
        if not DataTypeUtils.is_Int(req_data[DeviceConstant.device_id]):
            print "device_id is not Int" 
            return False

        if DeviceConstant.device_name in req_data:
            if not DataTypeUtils.is_String(req_data[DeviceConstant.device_name]):
                print "device_name is not String" 
                return False
    
        if DeviceConstant.device_type in req_data:
            if not DataTypeUtils.is_String(req_data[DeviceConstant.device_type]):
                print "device_type is not String" 
                return False
    
        if DeviceConstant.online in req_data:
            if not DataTypeUtils.is_Boolean(req_data[DeviceConstant.online]):
                print "online is not Boolean" 
                return False

        if DeviceConstant.user_id in req_data:
            if not DataTypeUtils.is_Int(req_data[DeviceConstant.user_id]):
                print "user_id is not Int" 
                return False

        if DeviceConstant.location in req_data:
            if not DataTypeUtils.is_String(req_data[DeviceConstant.location]):
                print "location is not String" 
                return False

        return req_data

    @staticmethod
    def is_post_param_ok(request):

        data = request.data
        try:  
            req_data = json.loads(data)
        except ValueError:  
            return False

        if not req_data \
                or not DeviceConstant.user_id in req_data:
            return False
         
        return req_data

    @staticmethod
    def is_post_param_with_wkb_ok(request):

        data = request.data
        try:
            req_data = json.loads(data)
        except ValueError:
            return False

        if not req_data \
                or not DeviceConstant.account_id in req_data \
                or not DeviceConstant.user_id in req_data \
                or not DeviceConstant.draw_wkb in req_data:
            return False

        return req_data

