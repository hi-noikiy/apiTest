# -*- coding: utf-8 -*-
__author__ = 'lily'
import os
import unittest
from common import util
from common.ReqLogin import req
from common import readYaml
from common import testLog

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

class SearchTest(ParametrizedTestCase):
    def setUp(self):
        self.searchCases = readYaml.getYam(r'E:\apiTest\YAML\web\case_search_api.yml')
        self.infoma = {}
        self.response = ""
        self.infoma["module"] = self.searchCases["testinfo"]["module"]
        self.infoma["intr"] = self.searchCases["testinfo"]["intr"]
        self.logTest = testLog.myLog().getLog()
    def test_search_api(self):
        self.infoma["id"] = self.param["id"]
        self.infoma["casename"] = self.param["casename"]
        util.DATA["sum"] = util.DATA["sum"] + 1
        self.response = req.reqData(req, url=self.param["api"], datas=self.param["data"])
        baseCheck = self.searchCases["Check"]
        try:
            if self.response["c"] == baseCheck["c"] and self.response["m"] == baseCheck["m"] and self.response["ok"] == baseCheck["ok"]:
                util.DATA["pass"] = util.DATA["pass"] + 1
                self.infoma["result"] = "通过"
                self.writeLog(self.param["casename"],flag=True,result="通过")
            else:
                util.DATA["fail"] = util.DATA["fail"] + 1
                self.infoma["result"] = "失败"
                # self.infoma["reason"] = "断言预期与实际不符"
                self.infoma["reason"] = self.response["m"]
                self.writeLog(self.param["casename"],flag=False,result="失败"+self.response["m"])

        except:
            util.DATA["fail"] = util.DATA["fail"] + 1
            self.infoma["result"] = "失败"
            self.infoma["reason"] = self.response["message"]
            self.writeLog(self.param["casename"], flag=False, result="异常"+self.response["message"])

        util.INFO.append(self.infoma)

    def writeLog(self,caseName,flag,result):
        if flag == True:
            self.logTest.buildStartLine(caseName + "++++++++成功")
            self.logTest.resultOK(caseName)
        else:
            self.logTest.buildStartLine(caseName + "------失败")
            self.logTest.resultNG(caseName,result)
        # self.logTest.buildEndLine(caseName + "结束了")
class HomeTest(ParametrizedTestCase):
    def setUp(self):
        self.getHomeCases = readYaml.getYam(r'E:\apiTest\YAML\web\case_home_api.yml')
        self.infoma = {}
        self.response = ""
        self.infoma["module"] = self.getHomeCases["testinfo"]["module"]
        self.infoma["intr"] = self.getHomeCases["testinfo"]["intr"]
    def test_home_api(self):
        self.infoma["id"] = self.param["id"]
        self.infoma["casename"] = self.param["casename"]
        util.DATA["sum"] = util.DATA["sum"] + 1
        self.response = req.reqData(req, url=self.param["api"], datas=self.param["data"])
        baseCheck = self.getHomeCases["Check"]
        try:
            if self.response["c"] == baseCheck["c"] and self.response["m"] == baseCheck["m"] and self.response["ok"] == baseCheck["ok"]:
                util.DATA["pass"] = util.DATA["pass"] + 1
                self.infoma["result"] = "通过"
            else:
                util.DATA["fail"] = util.DATA["fail"] + 1
                self.infoma["result"] = "失败"
                self.infoma["reason"] = self.response["m"]
        except:
            util.DATA["fail"] = util.DATA["fail"] + 1
            self.infoma["result"] = "失败"
            self.infoma["reason"] = self.response["message"]
        util.INFO.append(self.infoma)
class UserinfoTest(ParametrizedTestCase):
    def setUp(self):
        self.userAPI = readYaml.getYam(r'E:\apiTest\YAML\web\case_user_api.yml')
        self.infoma = {}
        self.response = ""
        self.infoma["module"] = self.userAPI["testinfo"]["module"]
        self.infoma["intr"] = self.userAPI["testinfo"]["intr"]
    def test_user_api(self):
        self.infoma["id"] = self.param["id"]
        self.infoma["casename"] = self.param["casename"]
        util.DATA["sum"] = util.DATA["sum"] + 1
        self.response = req.reqData(req, url=self.param["api"], datas=self.param["data"])
        baseCheck = self.userAPI["Check"]
        try:
            if self.response["c"] == baseCheck["c"] and self.response["m"] == baseCheck["m"] and self.response["ok"] == \
                    baseCheck["ok"]:
                util.DATA["pass"] = util.DATA["pass"] + 1
                self.infoma["result"] = "通过"
            else:
                util.DATA["fail"] = util.DATA["fail"] + 1
                self.infoma["result"] = "失败"
                self.infoma["reason"] = self.response["m"]
        except:
            util.DATA["fail"] = util.DATA["fail"] + 1
            self.infoma["result"] = "失败"
            self.infoma["reason"] = self.response["message"]
        util.INFO.append(self.infoma)

