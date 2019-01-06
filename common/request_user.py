# -*- coding: utf-8 -*-
import json
from constant.user_constant import UserConstant
from utils.user_utils import UserUtils

class ReqUserCommon:
    def __init__(self):
        pass

    @staticmethod
    def is_post_param_ok(request):

        data = request.data
        try:
            req_data = json.loads(data)
        except ValueError:
            return False

        if not req_data \
                or not UserConstant.username in req_data \
                or not UserConstant.password in req_data:
            return False

        username = req_data[UserConstant.username]
        if not UserUtils.is_valid_username(username):
            return False

        return req_data
