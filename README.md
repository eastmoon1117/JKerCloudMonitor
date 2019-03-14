# JKerCloudMonitor

极客Go玩客云监工的服务端实现，可以管理多个玩客云账号

## 框架
使用了python的Flask+MongoDB，还可以方便爬虫,基本目录结构如下所示：
```
.
├── app
│   └── __init__.py
├── config.json
├── controllers
│   ├── __init__.py
│   ├── tasks.py
│   └── users.py
├── models
│   ├── device.py
│   ├── __init__.py
│   └── user.py
└── run.py
```
具体可参考之前的博客：
[Python学习之路--Flask+MongoDB搭建Restful Server](https://blog.csdn.net/eastmoon502136/article/details/79053484)

## 用户模块
位置：/controllers/user

 - 注册
 
首先我们要提供注册接口，用户进入的第一入口，可以手机号+验证码方式，考虑到验证码需要收费，就不整了。提供个手机号或者邮箱+密码的方式来注册

 - 登录
 
 用户登陆后可以存储用户信息，以及玩客云的账号可以和用户绑定起来
 - 其他
 
当然还需要修改密码，找回密码等等接口，这里就略过不写了

## 账号模块
位置：/controllers/account

云监工的主要功能就是监控管理所有的玩客云账号
 - 新增账号
 
增加一个玩客云账号，需要尝试登陆（这里区分手机号和邮箱登陆），若能登陆成功，则和绑定到对应的用户
 - 删除账号
 
若不需要监控该玩客云，则需要删除当前用户下的该账号，解除绑定
 - 获取账号

可以获取所有的万科云账号信息
 - 更新账号
 
修改玩客云的名字等

## 统计提取链克模块
位置：/controllers/device

统计模块主要是统计当前所有玩客云账号的设备信息，7日链克统计
 - 7日信息

获取所有玩客云账号，统计链克昨日总产量，昨日平均产量，本月产量，总产量，已提取的链克和未提取链克，近七日的产量等
- 提取链克

方便快速提取链克，不需要登录各个账号去提取，所以需要一键提取所有链克的功能，直接存入钱包，前提是各个账号的钱包都已经配置好了

## 玩客云接口模块
位置：/wky
 - 玩客云接口

主要是各个迅雷玩客云的接口
 - 爬虫获取链克当前价格


## 未开源模块
以上模块已经完全可以使用了，接下来的扩展还未开源，若项目没啥人关注就不开源了。

 - 邮件提醒模块
 
 邮件提醒就是玩客云如果离线了或者异常了，会给对应绑定的邮箱发送邮件，当然也可以验证码，不过验证码要收费就不再考虑了。

 - 本地轮询更新模块
 
 轮询所有的玩客云当前的状态，目前是2小时轮询一次，查看当前的离在线情况，并且同步更新最新的数据

 - 代理模块
 
 由于各个接口都是迅雷的，所以如果我们的服务器大量访问迅雷服务器的话，可能会被封，所以可以通过代理的方式去访问迅雷的接口，可以一次性使用10000甚至更多的代理，这样平均下来就类似一个ip地址登录一个设备


云监工中其实最主要的是破解玩客云的接口，模拟成手机网页等请求服务器来获取数据。
### 准备
 - 玩客云App
 - charles抓包工具

至于怎么抓包，这里就不讲了，这里随便找了一篇文章：[charles抓包](https://blog.csdn.net/dongyuxu342719/article/details/78933618)，照着操作基本上也就会了。

### 接口汇总
 - 登陆：https://account.onethingpcs.com/user/login?appversion=1.4.8    （POST）
 - 获取近期收益：https://account.onethingpcs.com/wkb/income-history    （POST）
 - 获取一个月收益记录：https://account.onethingpcs.com/wkb/income-history    （POST）
 - 提币记录：https://account.onethingpcs.com/wkb/outcome-history?page=0    （POST）
 - 链克信息：https://account.onethingpcs.com/info/query  (POST)
 - 设备信息：https://control.onethingpcs.com/listPeer?X-LICENCE-PUB=1&appversion=1.6.2&ct=2&sign=efbcfd2744cfd2308acd1551cf054dfd&userid=5458114&v=3 (GET)
 - 磁盘信息：https://control.onethingpcs.com/getUSBInfo?appversion=1.6.2&ct=2&deviceid=TgjNiUqA6469&sign=234e0b3586ab1f920f33e853ce9820eb&v=1 (GET)
 - 提币：https://account.onethingpcs.com/wkb/draw?appversion=1.6.2 （POST）

### 接口抓包分析
我们抓取设备信息相关的包，如下图：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190106152403404.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2Vhc3Rtb29uNTAyMTM2,size_16,color_FFFFFF,t_70)
它的host是
```
Host	https://control.onethingpcs.com
```
也就是请求的https的地址，

接着看出来是get请求，请求的url如下所示：
```
GET /listPeer?X-LICENCE-PUB=1&appversion=2.2.1&ct=2&sign=1fbb87357a71e379db26b3ac76743418&userid=5458114&v=9 HTTP/1.1
```
其中query string信息如下，因为是get请求，所以会跟在url中
```
X-LICENCE-PUB	1
appversion	2.2.1
ct	2
sign	1fbb87357a71e379db26b3ac76743418
userid	5458114
v	9
```
然后就是cookies信息,请求时会传过去
```
origin	2
sessionid	dc3dee9cbb367601e3483835c7eacc9b
userid	5458114
ct	2
```

返回的设备信息结果如下：
```json
{
	"result": [0, {
		"global_appearance": 1,
		"devices": [{
			"imported": "20180519",
			"device_sn": "OCPG121196469",
			"licence": "T0NQRzEyMTE5NjQ2OS9taXVfNTQ1ODExNC8xNTI2OTA0NzQ1",
			"coturn_online": 1,
			"ip_info": {
				"country": "中国",
				"city": "杭州市",
				"isp": "电信",
				"province": "浙江省"
			},
			"status": "online",
			"exception_name": "",
			"hardware_model": "WS1608",
			"area_code": "CN",
			"ip": "xxx.xxx.xxx.xxx",
			"features": {
				"miner": 0,
				"onecloud_coin": 1526904760
			},
			"device_type": "OneCloud",
			"exception_message": "",
			"system_version": "V1.7.2",
			"lan_ip": "192.168.31.213",
			"disconnect_time": 1546440107,
			"upgradeable": false,
			"account_type": "miu",
			"device_name": "eastmoon6469",
			"is_exp": false,
			"account_name": "",
			"bind_time": 1526904745,
			"connect_time": 1546440118,
			"peerid": "00226D5A5A74889X0030",
			"mac_address": "00:22:6D:5A:xx:xx",
			"broker_id": 226568,
			"account_id": "5458114",
			"product_id": 412,
			"system_name": "挖矿固件",
			"type": 0
		}]
	}],
	"rtn": 0
}
```
既然我们都获取到了其中的信息，那么我们就可以模拟请求了，看下已经写好的python方法：
```python
 # 设备信息
 # https://control.onethingpcs.com/listPeer?X-LICENCE-PUB=1&appversion=1.6.2&ct=2&sign=efbcfd2744cfd2308acd1551cf054dfd&userid=5458114&v=3 (GET)
 def getDeviceInfo(self, sessionid, userid):
     sign1 = dict(appversion='1.6.2', ct='2', userid=userid, v='3')
     sign = getSignForGet(sign1, sessionid)

     url = 'https://control.onethingpcs.com/listPeer?X-LICENCE-PUB=1&appversion=1.6.2&ct=2' + '&sign=' + sign + '&userid=' + userid + '&v=3'
     cookies = dict(sessionid=sessionid, userid=userid)
     r = proxy.get(url=url, data=None, cookies=cookies)
     datas = json_util.dumps(r.content.decode('utf-8'), ensure_ascii=False)
     return json.loads(datas)
```
当然其中的sessionid,userid是登录接口返回的，这里就不做分析了，可以参考登录接口的[源码](https://github.com/eastmoon1117/JKerCloudMonitor/blob/master/wky/wky_interface.py)。还有就是sign签名的获取。为了接口更安全，客户端传的参数和服务端解析有个签名的校验。这里参考了不朽玩客云的sign生成，并结合实际接口做了略微的调整，最后是md5加密的，具体可以参考[源码](https://github.com/eastmoon1117/JKerCloudMonitor/blob/master/wky/wky_interface.py)。


