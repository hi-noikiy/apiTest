# -*- coding: utf-8 -*-
__author__ = 'lily'

import sys
import unittest
import time, datetime
from TestCase.webCase.case_web_all import ParametrizedTestCase,SearchTest,HomeTest,UserinfoTest
from common import report
from common import util
import xlsxwriter
from common import readYaml
import os

sys.path.append("..")
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p))

userCase = readYaml.getYam(r'E:\apiTest\YAML\web\case_user_api.yml')
searchCases = readYaml.getYam(r'E:\apiTest\YAML\web\case_search_api.yml')
getHomeCases = readYaml.getYam(r'E:\apiTest\YAML\web\case_home_api.yml')

def _report(filename):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet("测试总况")
    worksheet2 = workbook.add_worksheet("测试详情")
    re = report.OperateReport(wd=workbook)
    re.init(worksheet, data=util.DATA)
    re.test_detail(worksheet2, data=util.INFO)
    print(util.DATA,util.INFO)
    util.DATA = {"title": "项目名称", "sum": 0, "pass": 0, "fail": 0, "test_date":"", "sum_time":""}
    util.INFO = []
    re.close()
'''运行首页的几个接口'''
def runnerCaseHome():
    starttime = datetime.datetime.now()
    suite = unittest.TestSuite()
    for h in range(len(getHomeCases["homePage"])):
        apiH = getHomeCases["homePage"][h]
        suite.addTest(ParametrizedTestCase.parametrize(HomeTest, param=apiH))
    unittest.TextTestRunner(verbosity=2).run(suite)
    endtime = datetime.datetime.now()
    util.DATA["sum_time"] = str((endtime - starttime).seconds) + "秒"
    util.DATA["test_date"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    _report("..\ExcelReport\homePageAPI.xlsx")

'''运行搜索的几个借口'''
def runnerCaseSearch():
    starttime = datetime.datetime.now()
    suite = unittest.TestSuite()
    for s in range(len(searchCases["searchAPI"])):
        apiS = searchCases["searchAPI"][s]
        suite.addTest(ParametrizedTestCase.parametrize(SearchTest, param=apiS))
    unittest.TextTestRunner(verbosity=2).run(suite)
    endtime = datetime.datetime.now()
    util.DATA["sum_time"] = str((endtime - starttime).seconds) + "秒"
    util.DATA["test_date"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    _report("..\ExcelReport\searchAPI.xlsx")

'''运行用户相关的几个接口'''
def runnerCaseUser():
    starttime = datetime.datetime.now()
    suite = unittest.TestSuite()
    for u in range(len(userCase["userAPI"])):
        apiS = userCase["userAPI"][u]
        suite.addTest(ParametrizedTestCase.parametrize(UserinfoTest, param=apiS))
    unittest.TextTestRunner(verbosity=2).run(suite)
    endtime = datetime.datetime.now()
    util.DATA["sum_time"] = str((endtime - starttime).seconds) + "秒"
    util.DATA["test_date"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    _report("..\ExcelReport\meAndUserAPI.xlsx")

if __name__ == '__main__':
    runnerCaseHome()
    runnerCaseSearch()
    runnerCaseUser()
    pass
