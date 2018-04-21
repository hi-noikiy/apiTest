import unittest
from common.ReqLogin import req
import os
import yaml
from common import util
from TestCase.runnerBase import TestInterfaceCase
import paramunittest

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
def getYam(homeyaml):
    try:
        with open(homeyaml, encoding='utf-8') as f:
            x = yaml.load(f)
            return x
    except FileNotFoundError:
        print(u"找不到文件")
x = getYam(PATH("./case_user_api.yml"))

class UserinfoTest(TestInterfaceCase):
    def setUp(self):
        login = req.reqData(req)
        self.infoma = {}
        self.response = ""
        self.infoma["id"] = x["testinfo"][0]["id"]
        self.infoma["module"] = x["testinfo"][0]["module"]
        self.infoma["intr"] = x["testinfo"][0]["intr"]

    def base_check(self):
        baseCheck = x["basecheck"]
        if self.response["c"] == baseCheck["c"] and self.response["m"] == baseCheck["m"]:
            return True
        else:
            util.DATA["fail"] = util.DATA["fail"] + 1
            self.infoma["result"] = "失败"
            self.infoma["reason"] = "接口未正确返回"
            return False

    def detailCkeck_list(self,case):
        if self.base_check() is True:
            if "list" in  self.response:
                util.DATA["pass"] = util.DATA["pass"] + 1
                self.infoma["result"] = "通过"
            else:
                util.DATA["fail"] = util.DATA["fail"] + 1
                self.infoma["result"] = "失败"
                self.infoma["reason"] = self.response["c"]
        self.infoma["casename"] = case["casename"]
        util.DATA["sum"] = util.DATA["sum"] + 1
        util.INFO.append(self.infoma)

    def detailCheck_id(self,case):
        if self.base_check() is True:
            if self.response["r"]["id"] == case["data"]["id"]:
                util.DATA["pass"] = util.DATA["pass"] + 1
                self.infoma["result"] = "通过"
            else:
                util.DATA["fail"] = util.DATA["fail"] + 1
                self.infoma["result"] = "失败"
                self.infoma["reason"] = "断言预期与实际不符"
        self.infoma["casename"] = case["casename"]
        util.DATA["sum"] = util.DATA["sum"] + 1
        util.INFO.append(self.infoma)


    '''正常测试'''
    def test_user_info_conrrect(self):
        case1 = x["userinfo"]["case1"]
        self.response = Login.req(Login,case1["api"],case1["data"])
        self.detailCheck_id(case1)
    #
    # '''异常测试--value字段长度不够'''
    # def test_user_info_poorvalue(self):
    #     case2 = x["userinfo"]["case2"]
    #     self.response = Login.req(Login, case2["api"], case2["data"])
    #     if self.check1() is True:
    #         if self.response["r"]["id"] != case2["data"]["id"]:
    #             util.DATA["pass"] = util.DATA["pass"] + 1
    #             self.infoma["result"] = "通过"
    #         else:
    #             util.DATA["fail"] = util.DATA["fail"] + 1
    #             self.infoma["result"] = "失败"
    #             self.infoma["reason"] = "断言预期与实际不符"
    #     self.infoma["casename"] = case2["casename"]
    #     util.DATA["sum"] = util.DATA["sum"] + 1
    #     util.INFO.append(self.infoma)
    # '''异常测试--接口所需参数为空'''
    # def test_user_info_poorkey(self):
    #     case3 = x["userinfo"]["case3"]
    #     self.response = Login.req(Login,case3["api"],case3["data"])
    #     if self.check1() is False:
    #         if self.response["massage"] == case3["massage"]:
    #             util.DATA["pass"] = util.DATA["pass"] + 1
    #             self.infoma["result"] = "通过"
    #         else:
    #             util.DATA["fail"] = util.DATA["fail"] + 1
    #             self.infoma["result"] = "失败"
    #             self.infoma["reason"] = "断言预期与实际不符"
    #     self.infoma["casename"] = case3["casename"]
    #     util.DATA["sum"] = util.DATA["sum"] + 1
    #     util.INFO.append(self.infoma)

    def test_user_item_conrrect(self):
        case1 = x["useritems"]["case1"]
        self.response = Login.req(Login, case1["api"], case1["data"])
        self.detailCkeck_list(case1)

    def test_user_projectboards(self):
        case1 = x["userprojectboards"]["case1"]
        self.response = Login.req(Login, case1["api"], case1["data"])
        self.detailCkeck_list(case1)
    def test_me_info(self):
        case1 = x["me"]["case1"]
        self.response = Login.req(Login, case1["api"], case1["data"])
        self.base_check(case1)
    def test_me_orders(self):
        case1 = x["me"]["case2"]
        self.response = Login.req(Login, case1["api"], case1["data"])
        self.detailCkeck_list(case1)

    def tearDown(self):
        quit = Login.req(Login,'http://192.168.4.15:8001/api/0.2/account/signout',datas='')

if __name__ =='__main__':
    suite = unittest.TestSuite()
    # tests = ['test_user_info_conrrect','test_user_info_poorvalue','test_user_info_poorkey']
    # suite.addTests(map(UserinfoTest,tests))
    # suite.addTest(UserItemsTest("test_user_item_conrrect"))

    filename = r'C:\Users\xp\Desktop\result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title=u'自动化测试报告',
        description=u'注册- -自动化测试报告')
    runner.run(suite)
