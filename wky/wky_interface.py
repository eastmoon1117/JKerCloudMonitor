# -*- coding: utf-8 -*-

import requests
import json

from bson import json_util

from models.account import Account
import sys

reload(sys)
sys.setdefaultencoding('utf8')
requests.packages.urllib3.disable_warnings()


def md5(s):
    import hashlib
    return hashlib.md5(s.encode('utf-8')).hexdigest().lower()


# 获取pwd值（密码MD5后加密再取MD5值）
def GetPwd(passwd):
    s = md5(passwd)
    s = s[0:2] + s[8] + s[3:8] + s[2] + s[9:17] + s[27] + s[18:27] + s[17] + s[28:]
    return md5(s)


# 获取sign值
def GetSign(body, k=''):
    l = []
    while len(body) != 0:
        v = body.popitem()
        l.append(v[0] + '=' + v[1])
    l.sort()
    t = 0
    s = ''
    while t != len(l):
        s = s + l[t] + '&'
        t += 1
    s = s + 'key=' + k
    signs = md5(s)
    return signs


# 获取sign值
def getSignForGet(body, k=''):
    l = []
    l.append('X-LICENCE-PUB' + '=' + '1')
    while len(body) != 0:
        v = body.popitem()
        l.append(v[0] + '=' + v[1])
    l.sort()
    t = 0
    s = ''
    while t != len(l):
        s = s + l[t] + '&'
        t = t + 1
    # ss = s[0: len(s)-1]
    ss = s + 'key=' + k
    sign = md5(ss)
    return sign


# headers = {'user-agent': "Mozilla/5.0"}
headers = {'user-agent': 'MineCrafter3/1.6.2 (iPhone; iOS 11.3.1; Scale/2.00)'}
headers1 = {'cache-control': 'no-cache'}


class WKYInterface:
    # MD5函数
    def __init__(self):
        pass

    # 登陆
    # https://account.onethingpcs.com/user/login?appversion=1.4.8    （POST）
    def login(self, username, password, login_type):
        phone = username
        imeiid = md5(username)[0:15].upper()
        deviceid = md5(username)[0:16].upper()
        pwd = password

        if login_type == 'Email':
            body = dict(deviceid=deviceid, imeiid=imeiid, mail=phone, pwd=pwd, account_type='5', phone_area='Email')
            sign = GetSign(body)
            body = dict(deviceid=deviceid, imeiid=imeiid, mail=phone, pwd=pwd, account_type='5', phone_area='Email',
                        sign=sign)
        elif login_type == 'Phone':
            body = dict(deviceid=deviceid, imeiid=imeiid, phone=phone, pwd=pwd, account_type='4')
            sign = GetSign(body)
            body = dict(deviceid=deviceid, imeiid=imeiid, phone=phone, pwd=pwd, account_type='4', sign=sign)

        url = 'https://account.onethingpcs.com/user/login?appversion=1.6.2'
        cookies = None
        r = requests.post(url=url, data=body, verify=False, headers=headers, cookies=cookies, timeout=10)
        sessionid = r.cookies.get('sessionid')
        userid = r.cookies.get('userid')
        result = json.loads(r.content.decode('unicode-escape'))

        account = Account()
        if result['iRet'] == 0:
            account.sessionid = sessionid
            account.user_id = userid
        return account

    # 获取近期收益
    # https://account.onethingpcs.com/wkb/income-history    （POST）
    def getIncome(self, sessionid, userid):
        body = dict(page='0', appversion='1.6.2')
        sign = GetSign(body)
        url = 'https://account.onethingpcs.com/wkb/income-history'
        body = dict(page='0', appversion='1.6.2', sign=sign)
        cookies = dict(sessionid=sessionid, userid=userid, origin='2')
        r = requests.post(url=url, data=body, verify=False, headers=headers, cookies=cookies, timeout=10)
        datas = json_util.dumps(r.content.decode('unicode-escape'), ensure_ascii=False)
        return json.loads(datas)

    # 获取一个月收益记录
    # https://account.onethingpcs.com/wkb/income-history    （POST）
    def getMonthIncome(self, last_month, sessionid, userid):
        url = 'https://account.onethingpcs.com/wkb/income-history?appversion=1.6.2'
        body = dict(appversion='1.6.2', last_month=last_month)
        sign = GetSign(body)
        body = dict(appversion='1.6.2', last_month=last_month, sign=sign)
        cookies = dict(sessionid=sessionid, userid=userid, origin='2')
        r = requests.post(url=url, data=body, verify=False, headers=headers, cookies=cookies, timeout=10)
        datas = json_util.dumps(r.content.decode('unicode-escape'), ensure_ascii=False)
        return json.loads(datas)

    # 提币记录
    # https://account.onethingpcs.com/wkb/outcome-history?page=0    （POST）
    def getCoinInfo(self, sessionid, userid):
        url = 'https://account.onethingpcs.com/wkb/outcome-history?page=0'
        body = None
        cookies = dict(sessionid=sessionid, userid=userid, origin='1')
        r = requests.post(url=url, data=body, verify=False, headers=headers, cookies=cookies, timeout=10)
        datas = json_util.dumps(r.content.decode('unicode-escape'), ensure_ascii=False)
        return json.loads(datas)

    # 信息
    # https://account.onethingpcs.com/info/query  (POST)
    def getInfo(self):
        url = 'https://account.onethingpcs.com/info/query'
        body = None
        r = requests.post(url=url, data=body, verify=False, timeout=10)
        datas = json_util.dumps(r.content.decode('unicode-escape'), ensure_ascii=False)
        return json.loads(datas)

    # 设备信息
    # https://control.onethingpcs.com/listPeer?X-LICENCE-PUB=1&appversion=1.6.2&ct=2&sign=efbcfd2744cfd2308acd1551cf054dfd&userid=5458114&v=3 (GET)
    def getDeviceInfo(self, sessionid, userid):
        sign1 = dict(appversion='1.6.2', ct='2', userid=userid, v='3')
        sign = getSignForGet(sign1, sessionid)

        url = 'https://control.onethingpcs.com/listPeer?X-LICENCE-PUB=1&appversion=1.6.2&ct=2' + '&sign=' + sign + '&userid=' + userid + '&v=3'
        cookies = dict(sessionid=sessionid, userid=userid)
        r = requests.get(url=url, verify=False, headers=headers, cookies=cookies)
        datas = json_util.dumps(r.content.decode('utf-8'), ensure_ascii=False)
        return json.loads(datas)

    # 磁盘信息
    # https://control.onethingpcs.com/getUSBInfo?appversion=1.6.2&ct=2&deviceid=TgjNiUqA6469&sign=234e0b3586ab1f920f33e853ce9820eb&v=1 (GET)
    def getDeviceUsbInfo(self, sessionid, userid, deviceid):
        sign1 = dict(appversion='1.6.2', ct='2', deviceid=deviceid, v='3')
        sign = GetSign(sign1, sessionid)

        cookies = dict(sessionid=sessionid, userid=userid)
        url = 'https://control.onethingpcs.com/getUSBInfo?appversion=1.6.2&ct=2' + '&deviceid=' + deviceid + '&sign=' + sign + '&v=3'
        r = requests.get(url=url, headers=headers, cookies=cookies, timeout=10)
        datas = json_util.dumps(r.content.decode('utf-8'), ensure_ascii=False)
        return json.loads(datas)

    # 提币
    # https://account.onethingpcs.com/wkb/draw?appversion=1.6.2
    def drawLTK(self, sessionid, userid, peerid, drawWkb):
        url = 'https://account.onethingpcs.com/wkb/draw?appversion=1.6.2'
        body = dict(gasType='2', appversion='1.6.2', drawWkb=drawWkb)
        sign = GetSign(body)
        body = dict(gasType='2', appversion='1.6.2', drawWkb=drawWkb, sign=sign)
        cookies = dict(origin='2', sessionid=sessionid, userid=userid, peerid=peerid)
        # print sessionid + ":" + userid + ":" + peerid + ":" + drawWkb +':' + sign
        r = requests.post(url=url, data=body, verify=False, headers=headers, cookies=cookies, timeout=10)
        datas = json_util.dumps(r.content.decode('unicode-escape'), ensure_ascii=False)
        return json.loads(datas)
