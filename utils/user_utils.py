# -*- coding: utf-8 -*-
import re
import hashlib


class UserUtils:
    def __init__(self):
        pass

    @staticmethod
    def is_valid_username(name):
        phone = re.compile(r'[1][^1269]\d{9}')
        email = re.compile(r'[^\._][\w\._-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+$')
        res = phone.match(name)
        if res:
            return True
        else:
            res = email.match(name)
            if res:
                return True
            else:
                return False

    @staticmethod
    def get_phone_area_by_name(name):
        phone = re.compile(r'[1][^1269]\d{9}')
        email = re.compile(r'[^\._][\w\._-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+$')
        res = phone.match(name)
        if res:
            return 'Phone'
        else:
            res = email.match(name)
            if res:
                return 'Email'
            else:
                return ''

    @staticmethod
    def is_valid_password(password):
        if re.match(r"^\s*([0-9a-fA-F]{2,2}:){5,5}[0-9a-fA-F]{2,2}\s*$", password):
            return True
        return False

    # 获取pwd值（密码MD5后加密再取MD5值）
    @staticmethod
    def get_pwd(password):

        s = hashlib.md5(password.encode('utf-8')).hexdigest().lower()
        s = s[0:2] + s[8] + s[3:8] + s[2] + s[9:17] + s[27] + s[18:27] + s[17] + s[28:]
        return hashlib.md5(s.encode('utf-8')).hexdigest().lower()
