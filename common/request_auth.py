# -*- coding: utf-8 -*-
from auth import Auth
from config import Config
from constant.auth_constant import AuthConstant


class ReqAuthCommon:
    @staticmethod
    def is_auth_ok(request):
        # type: (object) -> object
        headers = request.headers
        try:
            if 'Authorization' in headers:
                token = headers["Authorization"]
            else:
                raise ValueError
        except ValueError:
            return False

        payload = Auth.decode_app_token(token)
        try:
            if 'data' in payload and AuthConstant.token_app_key in payload['data']:
                app_key = payload['data'][AuthConstant.token_app_key]
                app_secret = payload['data'][AuthConstant.token_app_secret]
            else:
                raise ValueError
        except ValueError:
            return False

        if app_key != Config.APP_KEY or app_secret != Config.APP_SECRET:
            return False

        return True

    @staticmethod
    def is_auth_user_ok(request):
        # type: (object) -> object
        headers = request.headers
        try:
            if 'Authorization' in headers:
                token = headers["Authorization"]
            else:
                raise ValueError
        except ValueError:
            return -1

        payload = Auth.decode_auth_token(token)
        try:
            if 'data' in payload and AuthConstant.token_id in payload['data']:
                user_id = payload['data'][AuthConstant.token_id]
            else:
                raise ValueError
        except ValueError:
            return -1

        return user_id
