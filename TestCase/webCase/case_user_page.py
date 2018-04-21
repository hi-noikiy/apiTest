__author__ = 'lily'
# -*- coding: utf-8 -*-
import unittest
from common.ReqLogin import req
import os
from common import util
from common import readYaml

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
getCases = readYaml.getYam(PATH(r'E:\apiTest\YAML\data_user_page.yml'))
getHomeCases = readYaml.getYam(r'E:\apiTest\YAML\case_home_page.yml')


# login = Login.login(Login)

class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """
    def __init__(self, methodName='runTest', param=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.param = param
        self.infoma = {}
        self.response = ""
        self.infoma["id"] = getCases["testinfo"][0]["id"]
        self.infoma["module"] = getCases["testinfo"][0]["module"]
        self.infoma["intr"] = getCases["testinfo"][0]["intr"]

    @staticmethod
    def parametrize(testcase_klass, param=None):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        login = req.login(req)
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, param=param))
        return suite

##用法-testcase

class TestOne(ParametrizedTestCase):

    """查询类接口的断言统一返回没有带list的接口,传有id且返回带有id的接口"""
    # def test_something(self):
    #     self.response = Login.req(Login,url=self.param["api"],datas= self.param["data"])
    #     baseCheck = getCases["basecheck"]
    #     if self.response["c"] == baseCheck["c"] and self.response["m"]== baseCheck["m"]:
    #         if self.response["r"]["id"] == self.param["data"]["id"]:
    #             util.DATA["pass"] = util.DATA["pass"] + 1
    #             self.infoma["result"] = "通过"
    #         else:
    #             util.DATA["fail"] = util.DATA["fail"] + 1
    #             self.infoma["result"] = "失败"
    #             self.infoma["reason"] = "断言预期与实际不符"
    #     else:
    #         util.DATA["fail"] = util.DATA["fail"] + 1
    #         self.infoma["result"] = "失败"
    #         self.infoma["reason"] = "请求失败"
    #     self.infoma["casename"] = self.param["casename"]
    #     util.DATA["sum"] = util.DATA["sum"] + 1
    #     util.INFO.append(self.infoma)
    #
    # """查询类接口的断言统一返回带有list的接口"""
    # def test_select_api(self):
    #     self.response = Login.req(Login, url=self.param["api"], datas=self.param["data"])
    #     baseCheck = getCases["basecheck"]
    #     if self.response["c"] == baseCheck["c"] and self.response["m"] == baseCheck["m"]:
    #         if self.response["r"]["id"] == self.param["data"]["id"]:
    #             util.DATA["pass"] = util.DATA["pass"] + 1
    #             self.infoma["result"] = "通过"
    #         else:
    #             util.DATA["fail"] = util.DATA["fail"] + 1
    #             self.infoma["result"] = "失败"
    #             self.infoma["reason"] = "断言预期与实际不符"
    #     else:
    #         util.DATA["fail"] = util.DATA["fail"] + 1
    #         self.infoma["result"] = "失败"
    #         self.infoma["reason"] = "请求失败"
    #     self.infoma["casename"] = self.param["casename"]
    #     util.DATA["sum"] = util.DATA["sum"] + 1
    #     util.INFO.append(self.infoma)

    def test_home_api(self):
        self.response = req.reqData(req, url=self.param["api"], datas=self.param["data"])
        baseCheck = getHomeCases["basecheck"]
        if self.response["c"] == baseCheck["c"] and self.response["m"]:
            util.DATA["pass"] = util.DATA["pass"] + 1
            self.infoma["result"] = "通过"
            self.infoma["reason"] = self.response["m"]

        else:
            util.DATA["fail"] = util.DATA["fail"] + 1
            self.infoma["result"] = "失败"
            # self.infoma["reason"] = "断言预期与实际不符"
            self.infoma["reason"] = self.response["m"]
        self.infoma["casename"] = self.param["casename"]
        util.DATA["sum"] = util.DATA["sum"] + 1
        util.INFO.append(self.infoma)

class TestSecond(ParametrizedTestCase):
    def add(self):
        print(self.param)