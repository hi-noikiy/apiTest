
# -*- coding: utf-8 -*-
__author__ = 'lily'


import requests
cmsSession = requests.session()
pwd = 'http://sy.meijian.com:8008/sy/login'
datas = {
    'username': 'hll',
    'password': '111111'
}
headers = {'x-mj-from': 'web'}
cmsSession.post(pwd,datas,headers=headers)
class syWeb:
    def syWebReq(self,url, datas,**kwargs):
        response = cmsSession.post('http://sy.meijian.com:8008/%s' % url, datas,headers = kwargs["headers"])
        dic = response.json()
        return dic