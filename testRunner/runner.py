__author__ = 'lily'
# -*- coding: utf-8 -*-
import sys
import unittest


sys.path.append("..")
import time, datetime
from TestCase.webCase.case_user_page import ParametrizedTestCase
from TestCase.webCase.case_web_all import searchTest

# from TestCase.case_user_info import UserinfoTest
from common import report
from common import util
import xlsxwriter
from common import readYaml
import os


PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p))
# getCases = readYaml.getYam(r'E:\MeijianApiTest\YAML\case_user_api.yml')
# getHomeCases = readYaml.getYam(r'E:\MeijianApiTest\YAML\case_home_api.yml')
searchCases = readYaml.getYam(r'E:\MeijianApiTest\YAML\case_search_api.yml')


def _report():
    workbook = xlsxwriter.Workbook('ExcelReport.xlsx')
    worksheet = workbook.add_worksheet("测试总况")
    worksheet2 = workbook.add_worksheet("测试详情")
    re = report.OperateReport(wd=workbook)
    re.init(worksheet, data=util.DATA)
    re.test_detail(worksheet2, data=util.INFO)
    re.close()
def runnerCaseWeb():
    starttime = datetime.datetime.now()
    suite = unittest.TestSuite()
    # for i in range(len(getHomeCases["nodataAPI"])):
    #     paraX = getHomeCases["nodataAPI"][i]
    #     suite.addTest(ParametrizedTestCase.parametrize(TestOne, param=paraX))
    #     suite.addTest(ParametrizedTestCase.parametrize(TestSecond, param=paraX))

    for i in  range(len(searchCases["Params"])):
        paraX = searchCases["Params"][i]
        suite.addTest(ParametrizedTestCase.parametrize(searchTest, param=paraX))
    unittest.TextTestRunner(verbosity=2).run(suite)
    endtime = datetime.datetime.now()
    util.DATA["sum_time"] = str((endtime - starttime).seconds) + "秒"
    util.DATA["test_date"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # destory_database()

if __name__ == '__main__':
    runnerCaseWeb()
    _report()
    print(util.INFO)
    print(util.DATA)
    pass
