# -*- coding: utf-8 -*-
from bson import json_util
from flask import Response

from app import app

from controllers.api_urls import AppUrls
from wky.ltk_bbx_price import LTKBBXPrice
import sys

reload(sys)
sys.setdefaultencoding('utf8')


@app.route(AppUrls.API_LKT_PRICE_INFO, methods=['POST'])
def get_ltk_price_info():
    ltk_price = LTKBBXPrice()
    info = ltk_price.get_price()

    json_data = json_util.dumps({'code': 1, 'data': info}, ensure_ascii=False, sort_keys=True, indent=4)

    return Response(json_data, mimetype='application/json')
