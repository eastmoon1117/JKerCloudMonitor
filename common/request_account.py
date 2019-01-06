# -*- coding: utf-8 -*-
import json

from constant.account_constant import AccountConstant
from constant.user_constant import UserConstant
from utils.user_utils import UserUtils

class ReqAccountCommon:
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
                or not AccountConstant.account_id in req_data \
                or not AccountConstant.user_id in req_data:
            return False

        return req_data
