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
class activityTest(ParametrizedTestCase):
    def setUp(self):
        self.info = {}
        self.response = ""
        self.logTest = testLog.myLog().getLog()

    def activityCase(self):
        if self.param["path"] == "/sy/item/create":
            print('sssss')

        else:
            self.info["module"] = "领福利活动"
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

    def sendVerifyCode(self):
        para1 = {
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
    def checkVerifyCode(self):
        para1 = {
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
    def signUp(self):
        para1 = {
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

    def writeLog(self, caseName, flag, result):
        if flag == True:
            self.logTest.buildStartLine(caseName + "++++++++成功")
            self.logTest.resultOK(caseName)
        else:
            self.logTest.buildStartLine(caseName + "------失败")
            self.logTest.resultNG(caseName, result)