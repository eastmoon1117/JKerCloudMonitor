# -*- coding: utf-8 -*-
import json
import re

class DeviceUtils:
    def __init__(self):
        pass

    @staticmethod
    def is_valid_ip(ip):  
        if re.match(r"^\s*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s*$", ip): 
            return True  
        return False  
                        
    @staticmethod  
    def is_valid_mac(mac):  
        if re.match(r"^\s*([0-9a-fA-F]{2,2}:){5,5}[0-9a-fA-F]{2,2}\s*$", mac):
            return True  
        return False  

