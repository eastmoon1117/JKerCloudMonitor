# -*- coding: utf-8 -*-
from bson import json_util

__author__ = 'iccool'

from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException
import random
import re
from datetime import datetime
import time

import sys

reload(sys)

sys.setdefaultencoding('utf-8')

# 由于只爬取两个网页的内容，就直接将该两个网页放入列表中
url_ltk = 'https://www.aicoin.net.cn/symbols/bbxltketh'

class LTKBBXPrice:

    # 更换User-Agent
    def getHeaders(self):
        user_agent_list = [
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36',
            'Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
            'Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1',
            'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;SE2.XMetaSr1.0;SE2.XMetaSr1.0;.NETCLR2.0.50727;SE2.XMetaSr1.0)'
        ]
        index = random.randrange(0, len(user_agent_list))
        headers = {
            'User-Agent': user_agent_list[index]
        }
        return headers

    # 获取页面内容
    def getHtml(self, url):
        try:
            response = requests.get(url, headers=self.getHeaders())
            if response.status_code == 200:
                return response.text
        except RequestException:
            print('===request exception===')
            return None

    # 解析网页 获取价格
    def parse_html(self, html):
        try:
            soup = BeautifulSoup(html, 'lxml')
            price_eth = soup.find_all("div", attrs={'data-reactid': re.compile("271")})
            price_usd = soup.find_all("div", attrs={'data-reactid': re.compile("282")})
            return price_eth, price_usd
        except Exception:
            print('===parseHtml exception===')
            return None

    def get_price(self):
        html = self.getHtml(url_ltk)
        price_eth, price_usd = self.parse_html(html)
        out_data = {
            'eth': price_eth[0].string,
            'usdt': price_usd[0].string,
            'update_time': time.mktime(datetime.now().timetuple())
        }
        return out_data
