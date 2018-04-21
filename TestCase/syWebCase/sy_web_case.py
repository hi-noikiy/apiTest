# -*- coding: utf-8 -*-
__author__ = 'lily'
import os
import unittest
from common import util
from common.syLogin import syWeb
from common.cmsLogin import syCMS
from common import testLog
import json
import time
import pymongo

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class ParametrizedTestCase(unittest.TestCase):
    def __init__(self, methodName='runTest', param=None):

        super(ParametrizedTestCase, self).__init__(methodName)
        self.param = param
    @staticmethod
    def parametrize(testcase_klass, param=None):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, param=param))
        return suite

class syWebTest(ParametrizedTestCase):
    def setUp(self):
        self.info = {}
        self.response = ""
        self.logTest = testLog.myLog().getLog()
        self.brandId = '5a30dc4e17d086ac62e3ad43'

    def test_syItems(self):
        if self.param["path"] == "/sy/item/create":
            print('sssss')
            # paras = self.syItemCreate()
            # self.check(paras=paras, heasers={'content-type': 'application/json','x-mj-from':'web'})
        # elif self.param["path"] == "/sy/item/createdSyItems":
        #     paras = self.createSyItemsPara()
        #     self.check(paras=paras,heasers='')
        # elif self.param["path"] == "/sy/item/update":
        #     paras = self.syItemUpdate()
        #     self.check(paras=paras, heasers={'content-type': 'application/json'})
        # elif self.param["path"] == "/sy/item/batchSubmitAudit":
        #     paras = self.batchSubmitAudit()
        #     self.check(paras=paras, heasers='')
        # elif self.param["path"] == "/sy/item/waitForAuditSyItems":
        #     paras = self.waitForAuditSyItems()
        #     self.check(paras=paras, heasers='')
        # elif self.param["path"] == "/sy/item/batchCancelAudit":
        #     paras = self.batchCancelAudit()
        #     self.check(paras=paras, heasers='')
        # elif self.param["path"] == "/sy/item/batchDeleted":
        #     paras = self.batchDeleted()
        #     self.check(paras=paras, heasers='')
        # elif self.param["path"] == "/sy/item/modify":
        #     paras = self.syItemModify()
        #     self.check(paras=paras,heasers={'content-type': 'application/json'})
        else:
            self.info["module"] = "syWeb"
            self.info["id"] = self.param["id"]
            self.info["casename"] = self.param["name"]
            self.info["path"] = self.param["path"]
            util.DATA["sum"] = util.DATA["sum"] + 1
            util.DATA["notTest"] = util.DATA["notTest"] + 1
            self.info["result"] = "未测试"
            self.info["reason"] = ""
            util.INFO.append(self.info)

    def check(self,paras,heasers):
        for para in paras:
            self.info = {}
            self.info["module"] = "syWeb"
            self.info["id"] = self.param["id"]
            self.info["casename"] = self.param["name"]
            self.info["path"] = self.param["path"]
            util.DATA["sum"] = util.DATA["sum"] + 1
            self.response = self.response = syWeb.syWebReq(syWeb, url=self.param["path"], datas=para["data"],
                                                           headers=heasers)
            print(self.param["path"],para["data"])
            if self.response["m"] == para["check"]["m"] and self.response["ok"] == para["check"]["ok"]:
                util.DATA["pass"] = util.DATA["pass"] + 1
                self.info["result"] = "通过"
                self.info["reason"] = self.response["m"]
                self.writeLog(caseName=self.param["name"], flag=True, result="通过")
                util.INFO.append(self.info)
            else:
                util.DATA["fail"] = util.DATA["fail"] + 1
                self.info["result"] = "失败"
                self.info["reason"] = self.response["m"]
                self.writeLog(self.param["name"], flag=False, result="失败" + self.response["m"])
                util.INFO.append(self.info)
        return util.INFO

    def syItemModify(self):
        para1= {
            "id":"5a6848d917d03f34016a63e1",        #类型：String  必有字段  备注：单品id
            "price":0,                            #类型：Number  必有字段  备注：价格
            "priceUnit":"价格单位",                   #类型：String  必有字段  备注：价格单位
            "series":"系列",                       #类型：String  必有字段  备注：系列
            "name":"单品名称",                      #类型：String  必有字段  备注：无
            "material":115545                           #类型：Number  必有字段  备注：材质
        }
        para1 = json.dumps(para1)
        check1 = {
            'ok': True,
            'm': 'success'
        }
        para2 = {
            "id": "",  # 类型：String  必有字段  备注：单品id
            "price": 300,  # 类型：Number  必有字段  备注：价格
            "priceUnit": "价格单位",  # 类型：String  必有字段  备注：价格单位
            "series": "系列",  # 类型：String  必有字段  备注：系列
            "name": "单品名称",  # 类型：String  必有字段  备注：无
            "material": 1  # 类型：Number  必有字段  备注：材质
        }
        para2 = json.dumps(para2)
        check2 = {
            'ok': False,
            'm': '参数错误'
        }
        data1 = {'check': check1, 'data': para1}
        data2 = {'check': check2, 'data': para2}
        para = [data1,data2]
        return para

    def batchDeleted(self):
        # response = syWeb.syWebReq(syWeb, url='/sy/item/createdSyItems',
        #                           datas={'brandContainerId': self.brandId, 'limit': 30, 'offset': 0},
        #                           headers='')
        response = syWeb.syWebReq(syWeb, url='/sy/item/rejectedSyItems',
                                  datas={'brandContainerId': self.brandId, 'limit': 30, 'offset': 0},
                                  headers='')
        items = response["r"]["list"]
        ids = []
        for i in range(len(items)):
            id = items[i]["id"]
            ids.append(id)
        print(ids)
        para1 = {'ids': [ids[0]]}
        check1 = {
            'ok': True,
            'm': 'success'
        }
        data1 = {'check': check1, 'data': para1}
        para = [data1]
        return para

    def batchCancelAudit(self):
        response= syWeb.syWebReq(syWeb, url='/sy/item/waitForAuditSyItems', datas={'brandContainerId':self.brandId,'limit':30,'offset':0},headers='')
        items = response["r"]["list"]
        ids = []
        for i in range(len(items)):
            id = items[i]["id"]
            ids.append(id)
        print(ids)

        para1 ={'ids':[ids[0], ids[1]]}
        check1 = {
            'ok': True,
            'm': 'success'
        }
        data1 = {'check': check1, 'data': para1}
        para = [data1]
        return para

    def waitForAuditSyItems(self):
        para1 = {
            'brandContainerId': self.brandId,
            'offset': '0',
            'limit': '20'
        }
        check1 = {
            'ok': True,
            'm': 'success'
        }
        data1 = {'check': check1, 'data': para1}
        para = [data1]
        return para

    def batchSubmitAudit(self):
        response= syWeb.syWebReq(syWeb, url='/sy/item/createdSyItems', datas={'brandContainerId':self.brandId,'limit':'10','offset':'0'},headers='')
        items = response["r"]["list"]
        ids = []
        for i in range(len(items)):
            id = items[i]["id"]
            ids.append(id)
        para1 ={'ids':[ids[0], ids[1]]}
        check1 = {
            'ok': True,
            'm': 'success'
        }
        data1 = {'check': check1, 'data': para1}
        para = [data1]
        return para

    def syItemUpdate(self):
        para1 = {
            'id': '5a6856fd17d03f34016a63eb',  #正常的item的id
            'link': 'http://www.helili.com',
            'price': '355500',
            'model': '模型是啥是啥是啥',
            'brandId':10312,
            'imgs': ['87947adf761f41e9b8f3087c4284bea8.png'],
            'colorRates': [{"id": 10, "rate": 1}],
            'name':'hfdjgfhg',
            # 'name': time.strftime("%Y%m%d%H:%M:%S", time.localtime()),
            'category': '102'
        }
        para1 = json.dumps(para1)
        check1 = {
            'ok': True,
            'm': 'success'
        }
        data1 = {'check': check1, 'data': para1}
        para2 = {
            'id':'58a14827274978575523378b',  #随便输入的id
            'link': 'http://www.helili1.com',
            'price': '300',
            'model': '模型是啥是啥是啥',
            'imgs': ['87947adf761f41e9b8f3087c4284bea8.png'],
            'colorRates': [{"id": 10, "rate": 0.862893}, {"id": 100, "rate": 0.771415}, {"id": 5, "rate": 0.671336}],
            'name': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            'category': '102'
        }
        para2 = json.dumps(para2)
        check2 = {
            'ok': False,
            'm': '参数错误'
        }
        data2 = {'check': check2, 'data': para2}
        para = [data1, data2]
        return para

    def syItemCreate(self):
        para1 = {
            'brandContainerId':self.brandId,
            'link': 'http://www.helili1.com',
            'price': '',
            'model': 'lily的模型',
            'imgs': ['0771207d4c866e5e518f1e8825b26b32.png'],
            'colorRates': [{"id":10,"rate":0.862893},{"id":100,"rate":0.771415},{"id":5,"rate":0.671336}],
            'name': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            'category': '102',
            'style':'5',
            'material':'木头哈哈哈',
            'series':'木质系列',
            'designer':'lily',
            'outYears': 2018,
            'size':'1000*300 50*20 100*60',
            'customize': 2
        }
        para1 = json.dumps(para1)

        para3 = {
            'brandContainerId': self.brandId,
            'link': 'http://www.helili1.com',
            'price': '',
            'model': 'lily的模型',
            'imgs': ['4cfe6522078e21e8e86f90cbd8bbaf36.png'],
            'colorRates': [{"id": 10, "rate": 0.862893}, {"id": 100, "rate": 0.771415}, {"id": 5, "rate": 0.671336}],
            'name': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            'category': 126,
            'style': '3',
            'material': '木头',
            'series': '木质系列',
            'designer': 'lily',
            'outYears': 2018,
            'size': '一个大木头墩儿，炒鸡炒鸡超级大大的木头hhahhaa',
            'customize': 1
        }
        para3 = json.dumps(para3)

        check1 = {
            'ok': True,
            'm': 'success'
        }
        data1 = {'check':check1,'data':para1}
        data3 = {'check':check1,'data':para3}

        para2 = {
            'brandContainerId': self.brandId,
            'link': 'http://www.taobao.com',
            'price': '300',
            'model': 'hha',
            'imgs': ['87947adf761f41e9b8f3087c4284bea8.png'],
            'colorRates': [{"id": 10, "rate": 0.862893}, {"id": 100, "rate": 0.771415}, {"id": 5, "rate": 0.671336}],
            'name': 'lil',
            'category': '102'
        }
        para2 = json.dumps(para2)
        check2 = {
            'ok': True,
            'm': 'success'
        }
        data2 = {'check': check2, 'data': para2}
        para4 = {
            'brandContainerId': self.brandId,
            'link': 'http://www.helili1.com',
            'price': '',
            'model': '我模型',
            'imgs': ['87947adf761f41e9b8f3087c4284bea8.png'],
            'colorRates': [{"id": 10, "rate": 0.862893}, {"id": 100, "rate": 0.771415}, {"id": 5, "rate": 0.671336}],
            'name': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            'category': '103',
            'style': '3',
            'material': '木头',
            'series': '木质',
            'designer': 'lily',
            'outYears': 2018,
            'size': '一个大木头墩儿，炒鸡炒鸡超级大大的木头hhahhaa',
            'customize': 1
        }
        para4 = json.dumps(para4)
        data4 = {'check': check1, 'data': para4}

        para = [data1,data3,data2,data4,data3,data2,data1]
        return para

    def createSyItemsPara(self):
        para1 = {
            'brandContainerId': self.brandId,
            'offset':'0',
            'limit': 100
        }
        check1 = {
            'ok':True,
            'm':'success'
        }
        data1 = {'check': check1, 'data': para1}
        para2 = {
            'brandContainerId': '',
            'offset':'0',
            'limit':'30'
        }
        check2 = {
            'ok': False,
            'm': '参数错误'
        }
        data2 = {'check': check2, 'data': para2}
        para3 ={
            'brandContainerId': self.brandId,
            'offset':'0',
        }
        check3 = {
            'ok': True,
            'm': 'success'
        }
        data3 = {'check': check3, 'data': para3}
        para = [data1]
        return para

    def writeLog(self, caseName, flag, result):
        if flag == True:
            self.logTest.buildStartLine(caseName + "++++++++成功")
            self.logTest.resultOK(caseName)
        else:
            self.logTest.buildStartLine(caseName + "------失败")
            self.logTest.resultNG(caseName, result)

    # def syBrands(self):
    #     url = '/sy/brand/syBrands'
    #     datas = ''
    #     self.response = syWeb.syWebReq(syWeb, url=url, datas=datas,headers='')
    #     print(self.response["r"][0]["id"])

class syCmsTest(ParametrizedTestCase):
    def setUp(self):
        self.info = {}
        self.response = ""
        self.logTest = testLog.myLog().getLog()
        self.brandId = '58a14827e4b01513b923378b'

    def test_syItems(self):
        if self.param["path"] == "/sy/item/update":
            print('')
            # paras = self.syItemUpate()    #修改待提交审核单品
            # self.check(paras=paras, heasers={'content-type': 'application/json','x-mj-from':'web'})
        # elif self.param["path"] == "/sy/item/waitForAuditList":
        #     paras = self.syItemWaitForAuditList()
        #     self.check(paras=paras,heasers='')
        # elif self.param["path"] == "/sy/item/auditSyItems":
        #     paras = self.auditSyItems()
        #     self.check(paras=paras, heasers='')
        # elif self.param["path"] == "/sy/item/deleteUpdateRecord":
        #     paras = self.deleteUpdateRecord()
        #     self.check(paras=paras, heasers='')
        # elif self.param["path"] == "/sy/item/waitForAuditSyItems":
        #     paras = self.syItemWaitForAuditList()
        #     self.check(paras=paras, heasers='')
        # elif self.param["path"] == "/sy/item/updateRecords":
        #     paras = self.syItemUpdateRecords()
        #     self.check(paras=paras, heasers='')
        # elif self.param["path"] == "/sy/item/lock":
        #     paras = self.syItemLock()
        #     self.check(paras=paras, heasers='')
        # elif self.param["path"] == "/sy/item/extendLock":
        #     paras = self.syItemExtendLock()
        #     self.check(paras=paras,heasers='')

        else:
            self.info["module"] = "syWeb"
            self.info["id"] = self.param["id"]
            self.info["casename"] = self.param["name"]
            self.info["path"] = self.param["path"]
            util.DATA["sum"] = util.DATA["sum"] + 1
            util.DATA["notTest"] = util.DATA["notTest"] + 1
            self.info["result"] = "未测试"
            self.info["reason"] = ""
            util.INFO.append(self.info)

    def check(self,paras,heasers):
        for para in paras:
            self.info = {}
            self.info["module"] = "cmsSy"
            self.info["id"] = self.param["id"]
            self.info["casename"] = self.param["name"]
            self.info["path"] = self.param["path"]
            util.DATA["sum"] = util.DATA["sum"] + 1
            self.response = self.response = syCMS.syCMSReq(syCMS, url=self.param["path"], datas=para["data"],
                                                           headers=heasers)
            print(self.param["path"],para["data"])
            if self.response["m"] == para["check"]["m"] and self.response["ok"] == para["check"]["ok"]:
                util.DATA["pass"] = util.DATA["pass"] + 1
                self.info["result"] = "通过"
                self.info["reason"] = self.response["m"]
                self.writeLog(caseName=self.param["name"], flag=True, result="通过")
                util.INFO.append(self.info)
            else:
                util.DATA["fail"] = util.DATA["fail"] + 1
                self.info["result"] = "失败"
                self.info["reason"] = self.response["m"]
                self.writeLog(self.param["name"], flag=False, result="失败" + self.response["m"])
                util.INFO.append(self.info)
        return util.INFO

    '''
    大后台修改SY待审核的单品
    '''
    def syItemUpate(self):
        response = syCMS.syCMSReq(syCMS, url='/sy/item/waitForAuditSyItems',
                                  datas={'brandContainerId': self.brandId, 'limit': 30, 'offset': 0},
                                  headers='')
        items = response["r"]["list"]
        ids = []
        for i in range(len(items)):
            id = items[i]["id"]
            ids.append(id)
        print(ids)
        para1 = {
            "id": ids[0],        #类型：String  必有字段  备注：单品id
            'price':111,                            #类型：Number  必有字段  备注：价格
            "series":"我再后台改了系列",                      #类型：String  必有字段  备注：系列
            "name":"我再后台改了名称",                      #类型：String  必有字段  备注：无
            "material":'我在后台改了材质',                         #类型：Number  必有字段  备注：材质
            'customize': 1
        }
        para1 = json.dumps(para1)
        check1 = {
            'ok': True,
            'm': 'success'
        }
        para2 = {
            "id": ids[1],  # 类型：String  必有字段  备注：单品id
            "model": "我在后台改了型号",  # 类型：String  必有字段  备注：型号
            "style": 2,  # 类型：String  必有字段  备注：无
            "outyears": '1999', # 类型：Number  必有字段  备注：年份
            'designer': '我是设计师',
            'category': 105
        }
        para2 = json.dumps(para2)
        para3 = {
            "id": ids[2],  # 类型：String  必有字段  备注：单品id
            'brandId': 10312,
            'brandContainerId': self.brandId
        }
        para3 = json.dumps(para3)
        check2 = {
            'ok': False,
            'm': '参数错误'
        }
        data1 = {'check': check1, 'data': para1}
        data2 = {'check': check1, 'data': para2}
        data3 = {'check':check2, 'data':para3}
        para = [data1,data2,data3]
        return para

    def syItemWaitForAuditList(self):
        para= 2
        return para

    def auditSyItems(self):
        response = syCMS.syCMSReq(syCMS, url='/sy/item/waitForAuditList',
                                  datas={'brandContainerId': self.brandId, 'p': 1, 'l': 30},
                                  headers='')
        items = response["r"]["list"]
        ids = []
        for i in range(len(items)):
            id = items[i]["id"]
            ids.append(id)

        para1 = {
            'ids': [ids[0]],
            'pass': 'false',
            'notPassReason': 1,
        }
        # para1 = json.dumps(para1)
        para2 = {
            'ids': [ids[1]],
            'pass': 'false',
            'notPassReason': 2,
        }
        # para2 = json.dumps(para2)

        para3 = {
            'ids': [ids[2]],
            'pass': 'false',
            'notPassReason': 3,
        }
        # para3 = json.dumps(para3)
        para4 = {
            'ids': [ids[3]],
            'pass': 'false',
            'notPassReason': 4,
        }
        # para4 = json.dumps(para4)

        para5 = {
            'ids': [ids[4]],
            'pass': 'false',
            'notPassReason': 99,
            'remark': '我就是不想让你的的单品通过，假货'
        }
        # para5 = json.dumps(para5)

        check = {
            'ok': True,
            'm': 'success'
        }

        data1 = {'check': check, 'data': para1}
        data2 = {'check': check, 'data': para2}
        data3 = {'check': check, 'data': para3}
        data4 = {'check': check, 'data': para4}
        data5 = {'check': check, 'data': para5}
        para = [data1, data2, data3, data4, data5]
        return para

    def syItemUpdateRecords(self):
        para1 = {
            'p': 1,
            'l': 30
        }
        check1 = {
            'ok': True,
            'm': 'success'
        }
        data1 = {'check': check1, 'data': para1}
        para = [data1]
        return para

    def syItemLock(self):
        para = 2
        return para

    def syItemExtendLock(self):
        para = 2
        return para

    def deleteUpdateRecord(self):
        response = syCMS.syCMSReq(syCMS, url='/sy/item/updateRecords',datas={'p': 1, 'l': 30},headers='')
        items = response["r"]["list"]
        ids = []
        for i in range(len(items)):
            id = items[i]["id"]
            ids.append(id)
        print(ids)
        para = {
            'id': ids[0]
        }
        check ={
            'ok': True,
            'm': 'success'
        }
        data1 = {'check': check, 'data': para}
        para = [data1]
        return para

    def writeLog(self, caseName, flag, result):
        if flag == True:
            self.logTest.buildStartLine(caseName + "++++++++成功")
            self.logTest.resultOK(caseName)
        else:
            self.logTest.buildStartLine(caseName + "------失败")
            self.logTest.resultNG(caseName, result)




