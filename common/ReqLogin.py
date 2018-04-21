# -*- coding: utf-8 -*-

__author__ = 'lily'
import requests
session = requests.session()
pwd = 'http://app.meijian.io/api/0.2/account/signin/pwd'
datas = {
    'username': '18258183861',
    'pwd': '666666'
}
session.post(pwd,datas)
class req:
    def reqData(self,url, datas) :
        response = session.post('http://app.meijian.io/api/0.2/%s' % url, datas)
        dic = response.json()
        return dic
    # def login(self):
    #     pwd = 'account/signin/pwd'
    #     datas = {
    #         'username': '18258183861',
    #         'pwd': '666666'
    #     }
    #     self.reqData(self,pwd,datas)
