# -*- coding: utf-8 -*-
__author__ = 'lily'
import requests
import json
from common import report
from common import util
import xlsxwriter

class GetURL:
    def __init__(self):
        self.session = requests.session()
        self.DOCleverLogin()
        self.response = ""

    def baseData(self):
        # syServerUrl = 'http://192.168.1.75:12580/project/interface?id=5a5da326034fb1b157cce238&sort=1'
        # sprint14Url = 'http://192.168.1.75:12580/project/interface?id=5a7a6cbc62f4b5554ea4e86b&sort=1'
        # H5Activity = 'http://192.168.1.75:12580/project/interface?id=5a9908a862f4b5554ea4e923&sort=1'
        mobileV1='http://192.168.1.75:12580/project/interface?id=5a575a76034fb1b157cce1ce&sort=1'
        response = self.httpRequest(url=mobileV1, param='', method="get")
        dicInfo_dump = json.dumps(response, sort_keys=True, indent=10, ensure_ascii=False)
        dicInfo = json.loads(dicInfo_dump)
        # cmsUrl = dicInfo["data"]["data"][1]["data"]
        # syUrl = dicInfo["data"]["data"][2]["data"]
        baseProject = dicInfo["data"]["data"][1]["data"]
        for i in range(len(baseProject)):
            self.urlInfo = {}
            self.urlInfo["module"] = dicInfo["data"]["data"][1]["name"]
            self.urlInfo["method"] = "post"
            self.urlInfo["id"] = baseProject[i]["_id"]
            self.urlInfo["finish"] = baseProject[i]["finish"]
            self.urlInfo["name"] = baseProject[i]["name"]
            self.urlInfo["path"] = baseProject[i]["url"]
            params = self.detailData(self.urlInfo["id"])
            self.urlInfo["param"] = str(params)
            util.INFO.append(self.urlInfo)
        _report("..\GetURLInfo\BaseUrlExcel\大上海H5活动.xlsx")

    def detailData(self, urlId):
        url = 'http://192.168.1.75:12580/interface/item?id=%s' % urlId
        detail = self.httpRequest(url=url,param='',method="get")
        param = []
        # if detail["data"]["group"]["name"] == "elink":
        #     body = detail["data"]["param"][0]["queryParam"]
        #     for raw in body:
        #         raw = {raw["name"]: raw["remark"]}
        #         param.append(raw)
        #     return param
        # if detail["data"]["group"]["name"] == "主应用相关cps接口":
        #     if len(detail["data"]["param"][0]["bodyParam"]) != 0:
        #         body = detail["data"]["param"][0]["bodyParam"]
        #         for raw in body:
        #             raw = {raw["name"]: raw["remark"]}
        #             param.append(raw)
        #         return param
        #     else:
        #         body = detail["data"]["param"][0]["queryParam"]
        #         for raw in body:
        #             raw = {raw["name"]: raw["remark"]}
        #             param.append(raw)
        #         return param
        # if detail["data"]["group"]["name"] == "大后台相关cps接口":
        #     if detail["data"]["method"] == "GET":
        #         body = detail["data"]["param"][0]["queryParam"]
        #         for raw in body:
        #             raw = {raw["name"]: raw["remark"]}
        #             param.append(raw)
        #         return param
        #     elif len(detail["data"]["param"][0]["bodyParam"]) !=0:
        #         body = detail["data"]["param"][0]["bodyParam"]
        #         for raw in body:
        #             raw = {raw["name"]: raw["remark"]}
        #             param.append(raw)
        #         return param
        #     else:
        #         param = ''
        #         return param
        if detail["data"]["group"]["name"] == "领福利活动":
            if len(detail["data"]["param"][0]["bodyParam"]) != 0:
                body = detail["data"]["param"][0]["bodyParam"]
                for raw in body:
                    raw = {raw["name"]: raw["remark"]}
                    param.append(raw)
                return param
            else:
                body = detail["data"]["param"][0]["queryParam"]
                for raw in body:
                    raw = {raw["name"]: raw["remark"]}
                    param.append(raw)
                return param
        else:
            param = ''
            return param

    def httpRequest(self,url,param,method):
        if method =="post":
            self.response = self.session.post(url=url,data=param)
        else:
            self.response = self.session.get(url=url)
        dicInfo = self.response.json()
        return dicInfo

    def DOCleverLogin(self):
        loginUrl = 'http://192.168.1.75:12580/user/login'
        datas = {
            'name' : 'helili',
            'password':'666666'
        }
        self.response= self.httpRequest(url=loginUrl, param=datas, method="post")
        if self.response["msg"] == "ok":
            print("login success")
        else:
            print(self.response["msg"])

def _report(filename):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet("测试详情")
    re = report.OperateReport(wd=workbook)
    re.baseUrl(worksheet, data=util.INFO)
    print(util.INFO)
    util.INFO = []
    re.close()

if __name__ == '__main__':
    getUrl = GetURL()
    getUrl.baseData()
