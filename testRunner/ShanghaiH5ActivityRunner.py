# -*- coding: utf-8 -*-
__author__ = 'lily'

import sys
import unittest


sys.path.append("..")
import time, datetime
from TestCase.ShanghaiH5Activity.case_activity_api import ParametrizedTestCase,activityTest
from common import report
from common import util
import xlsxwriter
from common import readExcel
import os

import json


PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p))

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
def runnerCaseActivity():
    cases = readExcel.getExcel("E:\yongli\ShanghaiH5Activity\interface\上海H5活动.xlsx")
    starttime = datetime.datetime.now()
    suite = unittest.TestSuite()
    for case in cases:
        suite.addTest(ParametrizedTestCase.parametrize(activityTest, param=case))
    unittest.TextTestRunner(verbosity=2).run(suite)
    endtime = datetime.datetime.now()
    util.DATA["sum_time"] = str((endtime - starttime).seconds) + "秒"
    util.DATA["test_date"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    _report("..\ExcelReport\ActivityReport\Activity.xlsx")


if __name__ == '__main__':
    runnerCaseActivity()
    pass
