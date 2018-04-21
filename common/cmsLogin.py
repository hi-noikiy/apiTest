# -*- coding: utf-8 -*-

__author__ = 'lily'
import requests
syCmsSession = requests.session()
pwd = 'http://cms.meijian.com:8003/api/admin/login'
datas = {
    'username': 'admin',
    'password': '111111'
}
syCmsSession.post(pwd,datas)
class syCMS:
    def syCMSReq(self,url, datas,**kwargs) :
        response = syCmsSession.post('http://cms.meijian.com:8003/api/%s' % url, datas,headers = kwargs["headers"])
        dic = response.json()
        return dic