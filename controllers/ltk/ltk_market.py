# -*- coding: utf-8 -*-
from bson import json_util
from flask import Response
from flask import json

from app import app

from controllers.api_urls import AppUrls
from wky.wky_interface import WKYInterface
import sys

reload(sys)
sys.setdefaultencoding('utf8')


@app.route(AppUrls.API_LKT_MARKET_INFO, methods=['POST'])
def get_ltk_market_info():
    wky = WKYInterface()
    info = wky.getInfo()

    response = json.loads(info)

    json_data = json_util.dumps({'code': 1, 'data': response}, ensure_ascii=False, sort_keys=True, indent=4)

    return Response(json_data, mimetype='application/json')
